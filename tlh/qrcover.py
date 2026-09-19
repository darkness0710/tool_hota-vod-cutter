"""Find the donation QR once, so the renderer can paint over it everywhere.

The QR is not a moving object. OBS burns it into the stream at one fixed
position and leaves it there: measured on [1-Af2IFi77o], the crop at
(1787, 453, 124, 124) is pixel-identical across twenty samples spanning ten
minutes -- correlation 0.999 or better against the first one at every single
sample, with no frame where it is absent.

That fact is what decides the design, because cv2.QRCodeDetector is nowhere
near reliable enough to run per frame. On those same twenty frames, with the
code provably present and provably unchanged, it detected only NINE. A cover
driven by per-frame detection would therefore leave the QR exposed on more
than half the frames -- worse than not covering at all, because it looks done.

So the QR is found ONCE over a handful of frames, grown to the white card it
is printed on, grown again by a safety factor, and that one rectangle is
painted over every segment at render time. Detection failing is not fatal: the
card sits against the right edge, level with the minimap, in every VOD seen, so
a miss falls back to that rectangle with a wider margin and says so loudly.
"""
import subprocess
import time

import cv2
import numpy as np

from . import config as C
from .ffmpeg import grab, hms

# Everything here works in the SOURCE's own pixels, not the reference frame
# the detector uses. The rectangle it produces is handed to the renderer, which
# never rescales the video, so it has to be in the coordinates the renderer
# will paint in. Detection needs no reference size of its own: a QR is found by
# its own geometry at whatever size it is drawn.

HEARTBEAT = 5.0         # seconds between progress lines while scrubbing


def _card(gray, box, frame):
    """Grow a QR box out to the white card it is printed on.

    The card is the code's white quiet zone, a little larger than the modules
    the detector reports: 131x140 against a reported 124x124 on [1-Af2IFi77o].
    Covering the modules alone would leave a thin white border framing the
    cover, which reads as a mistake rather than as a logo.

    Each edge is found by profiling whiteness ACROSS the code's own span on
    the other axis, then taking the run of rows (or columns) that is white and
    CONTIGUOUS with the code. Both halves of that matter, and each was learned
    by getting it wrong:

    * Restricting the profile to the code's span is what separates the
      populations -- a card column is 100% white, the code's own columns about
      50% because half a QR is black, the Heroes sidebar behind it 0-10%.
      Profiling over a generous window instead diluted a card column to 57%,
      a hair over any threshold, and returned 140x140.

    * Contiguity is what keeps the card out of the sidebar. The sidebar has
      gold trim of its own at x=1716 that is also 100% white; it is not part
      of the card, and the only thing that says so is the dark gap at
      x 1724..1772 between them. Taking the connected white component instead
      jumped that kind of gap elsewhere and returned 140x284.

    Note what this does NOT do: grow to some panel behind the code. There is
    no panel. The white square sits straight on the Heroes sidebar, which is
    why an early hand measurement of a "200x140 card" was wrong -- it had swept
    up that gold trim -- and why the numbers it produced are not to be trusted
    as a check on this function.
    """
    x, y, w, h = box
    fw, fh = frame
    pad = 80
    x0, y0 = max(0, x - pad), max(0, y - pad)
    x1, y1 = min(fw, x + w + pad), min(fh, y + h + pad)
    white = gray > 200

    def run(profile, lo, hi):
        """Extent of the True run in `profile` that spans lo..hi."""
        a = lo
        while a > 0 and profile[a - 1]:
            a -= 1
        b = hi
        while b < len(profile) - 1 and profile[b + 1]:
            b += 1
        return a, b

    cols = white[y:y + h, x0:x1].mean(0) > C.QR_CARD_WHITE
    rows = white[y0:y1, x:x + w].mean(1) > C.QR_CARD_WHITE
    ca, cb = run(cols, x - x0, x + w - 1 - x0)
    ra, rb = run(rows, y - y0, y + h - 1 - y0)
    return x0 + ca, y0 + ra, cb - ca + 1, rb - ra + 1


def _grow(box, factor, frame):
    """Scale a box about its own centre, clamped to the frame.

    Even x/y/w/h, because the source is yuv420p and ffmpeg rounds an odd crop
    or overlay offset down -- silently, and by a pixel that would show as a
    white seam along the edge of the cover.
    """
    x, y, w, h = box
    fw, fh = frame
    cx, cy = x + w / 2.0, y + h / 2.0
    w, h = w * factor, h * factor
    x0 = max(0, int(cx - w / 2)) // 2 * 2
    y0 = max(0, int(cy - h / 2)) // 2 * 2
    x1 = min(fw, int(cx + w / 2) + 1) // 2 * 2
    y1 = min(fh, int(cy + h / 2) + 1) // 2 * 2
    return x0, y0, x1 - x0, y1 - y0


def find(video, dur, frame, progress=print):
    """Rectangle to paint over, as (x, y, w, h) in `frame` pixels.

    Never returns None.

    Samples across the WHOLE video rather than the opening minutes: a stream
    opens on a "starting soon" card or the HotA lobby, where the overlay may
    not be up yet, and the first frames are the least representative ones
    there are.
    """
    step = dur / (C.QR_SAMPLES + 1)
    for k in range(1, C.QR_SAMPLES + 1):
        # At the source's own size. grab() defaults to 1920x1080 and sizes its
        # read buffer from that, so a 2560x1440 frame came back as a stride's
        # worth of the wrong bytes -- on which the detector duly "found" a
        # 738x794 QR and the renderer painted the logo across the middle of
        # the game while the real code sat untouched at the edge.
        shot = grab(video, step * k, size=frame)
        if shot is None:
            continue
        det = cv2.QRCodeDetector()
        ok, pts = det.detect(shot)
        if not ok:
            continue
        # DECODING is the proof, not detecting. detect() returns a quad for
        # things that are not codes at all -- measured on a scrubbed file it
        # claimed one on 3 of 30 frames where the code had been painted over --
        # and this loop returns on the first hit, so one false positive early
        # on wins over every real code after it. On a 2560x1440 file that put
        # the cover at 1030x604 in the middle of the game while the real code
        # sat untouched at 2383,604. A payload cannot be hallucinated.
        try:
            if not det.decode(shot, pts)[0]:
                continue
        except cv2.error:
            continue
        p = pts.reshape(-1, 2)
        box = (int(p[:, 0].min()), int(p[:, 1].min()),
               int(p[:, 0].max() - p[:, 0].min()),
               int(p[:, 1].max() - p[:, 1].min()))
        gray = cv2.cvtColor(shot, cv2.COLOR_BGR2GRAY)
        card = _card(gray, box, frame)
        rect = _grow(card, C.QR_BUFFER, frame)
        progress(f"        QR found at {box[0]},{box[1]} {box[2]}x{box[3]}"
                 f"  -> card {card[2]}x{card[3]}"
                 f"  -> covering {rect[2]}x{rect[3]} at {rect[0]},{rect[1]}")
        return rect

    # Detection is flaky enough that this is a normal outcome, not a bug: it
    # missed 11 of 20 frames on a code that never moved. The card lives in the
    # same corner in every VOD seen, so cover that corner with a wider margin
    # and carry on -- loudly. Stopping here would be the more defensible
    # choice for a privacy cover, and it was the recommendation; continuing
    # with a blind rectangle is the owner's call, on the grounds that a
    # too-large cover costs nothing but a hidden QR costs everything.
    # C.QR_CARD is measured in C.REF, so on any other frame it has to be
    # scaled before it means anything.
    ratio = frame[0] / C.REF[0]                 # not k: that is the loop index
    blind = tuple(int(v * ratio) for v in C.QR_CARD)
    rect = _grow(blind, C.QR_BUFFER_BLIND, frame)
    progress(f"        WARNING: no QR decoded in {C.QR_SAMPLES} samples. "
             f"Covering the usual corner blind, with the wider "
             f"{C.QR_BUFFER_BLIND}x margin: {rect[2]}x{rect[3]} at "
             f"{rect[0]},{rect[1]}. CHECK THE OUTPUT before publishing it.")
    return rect


def scrub(src, dst, progress=print):
    """Re-encode `src` to `dst` with the code painted over. Returns 0 on success.

    A whole-file re-encode, because there is no cheaper way: pixels can only be
    replaced by encoding them again. It reuses render.py's encoder choice and
    quality so a scrubbed file matches a cut one, and copies the audio rather
    than re-encoding it -- nothing here touches sound.

    Progress comes from ffmpeg's own -progress stream rather than from parsing
    stderr: stderr's stats line is redrawn with \r and carries no total, so a
    percentage would have to be reconstructed from it. out_time_us against the
    duration already known is exact.
    """
    from . import encoder                       # local: pulls in probing
    from .ffmpeg import FF, duration, size as ffmpeg_size

    # Checked here rather than left to ffmpeg. Missing, it fails as an input
    # error from a command line the reader never typed, halfway down a log --
    # against which "the file is not there" is the whole of the problem.
    if not C.QR_COVER.exists():
        progress(f"    no cover image at {C.QR_COVER}")
        return 1

    total = duration(str(src)) or 0.0
    frame = ffmpeg_size(str(src)) or C.REF
    rect = find(str(src), total, frame, progress=progress)
    x, y, w, h = rect
    codec, qflag = encoder.detect(log=progress)
    cmd = ([FF, "-v", "error", "-progress", "pipe:1", "-nostats",
            "-i", str(src), "-i", str(C.QR_COVER),
            "-filter_complex",
            f"[1:v]scale={w}:{h}:force_original_aspect_ratio=increase,"
            f"crop={w}:{h}[cov];"
            f"[0:v][cov]overlay={x}:{y}:eof_action=repeat,format=yuv420p[v]",
            "-map", "[v]", "-map", "0:a?", "-c:v", codec]
           + encoder.quality_args(qflag)
           + ["-c:a", "copy", "-movflags", "+faststart", "-y", str(dst)])

    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    started, last = time.time(), -HEARTBEAT
    try:
        for raw in proc.stdout:
            line = raw.decode("utf-8", "replace").strip()
            if not line.startswith("out_time_us=") or not total:
                continue
            try:
                done = int(line.split("=", 1)[1]) / 1e6
            except ValueError:
                continue
            now = time.time() - started
            if now - last < HEARTBEAT:
                continue
            last = now
            pct = min(99, int(100 * done / total))
            rate = done / now if now > 0 else 0.0
            left = (total - done) / rate if rate > 0.01 else 0.0
            progress(f"    qr {pct:3d}%   {hms(done)} of {hms(total)}"
                     + (f"   eta {hms(left)}" if left else ""))
    finally:
        proc.stdout.close()
    code = proc.wait()
    if code == 0:
        progress(f"    qr 100%   {hms(total)} of {hms(total)}")
    return code
