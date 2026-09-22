"""Run the whole thing for one video."""
import json
import os
import time

import numpy as np

from . import config as C
from . import render as render_mod
from . import naming, qrcover, screens, segments as seg_mod
from . import signal as signal_mod
from . import timeline
from .ffmpeg import (duration, frame_rate, hms, scale_to,
                     size as probe_size)


def _log(*args):
    """Progress must be unbuffered: these runs take tens of minutes, and a
    buffered stdout shows nothing at all until the process exits."""
    print(*args, flush=True)


def _signal_fingerprint(prescale=""):
    """Identity of everything that changes what the signal pass produces.

    Cached signal is reused only when this matches, so editing a coordinate in
    config.py or rebuilding the name template invalidates the cache instead of
    silently reusing numbers that no longer mean the same thing. Thresholds are
    deliberately excluded: they are applied downstream in interpret(), so they
    can be retuned against a cached signal.
    """
    stamps = []
    for name in ("tieulinh_name.png", "spell_left.png", "spell_right.png",
                 "digits.npz"):
        path = C.TEMPLATES / name
        stamps.append(path.stat().st_mtime_ns if path.exists() else 0)
    # The column layout belongs in here. Without it, removing a column left the
    # old wider array passing the check and being read with the new indices --
    # harmless only because the dropped columns happened to be last.
    # prescale belongs in here even though a video's size never changes: a
    # cache written before the detector learned to scale holds numbers read at
    # the wrong stride, and nothing else in this tuple would notice.
    return repr((signal_mod.COLUMNS, prescale,
                 C.SR, C.CLK, C.UPPER_BAND, C.LOWER_BAND, C.NAME_L, C.NAME_R,
                 C.DAY, C.DIGIT_X, C.DIGIT_Y, C.GLYPH_H, C.GLYPH_W_MIN,
                 C.SPELL_L, C.SPELL_R, tuple(stamps)))


def _load_signal(path, prescale=""):
    if not os.path.exists(path):
        return None
    try:
        blob = np.load(path, allow_pickle=False)
        if str(blob["fingerprint"]) != _signal_fingerprint(prescale):
            return None
        return blob["sig"]
    except Exception:
        return None                             # corrupt or old format: redo it


def process_video(video, out, workdir, workers=4, render_workers=3,
                  dry_run=False, reuse_signal=True, keep_parts=False,
                  parts_only=False, per_game=False, min_game=0.0,
                  log=_log):
    """Analyse `video`, write the cut to `out`. Returns an exit code.

    `workdir` holds this video's scratch: the segment list and the rendered
    pieces. Keeping it per-video is what lets a batch run be interrupted and
    resumed without two files trampling each other.
    """
    os.makedirs(workdir, exist_ok=True)
    dur = duration(video)

    # Read the source size ONCE, here, and tell the reader what it is. Every
    # coordinate in config.py is measured in C.REF, so anything else is scaled
    # to C.REF for detection -- and only for detection: the render never
    # rescales, so a 1440p VOD comes out 1440p.
    #
    # This used to be checked only on the download path, which meant a file
    # dropped into input/ by hand was never measured at all. A 1440p one then
    # read zero clocks, zero name plates and zero day counters, cut nothing,
    # and the only clue was a warning about the clock coordinates.
    frame = probe_size(video) or tuple(C.REF)
    prescale = scale_to(frame, C.REF)
    fps = frame_rate(video) or "30"
    if tuple(frame) != tuple(C.REF):
        ar, ref_ar = frame[0] / frame[1], C.REF[0] / C.REF[1]
        if abs(ar - ref_ar) > C.AR_TOL:
            log(f"    frame     {frame[0]}x{frame[1]}   ty le {ar:.2f}")
            log(f"    Khung hinh nay khong phai 16:9. Thu nho ve "
                f"{C.REF[0]}x{C.REF[1]} se lam meo hinh va khong toa do nao "
                "con dung, nen file nay bi tu choi thay vi cat sai.")
            return 2
    signal_s = dur / C.RATE_SIGNAL
    screens_s = dur * C.RATE_SCREENS
    render_s = 0.0 if dry_run else dur * C.KEEP_GUESS / C.RATE_RENDER
    log(f"    file      {os.path.basename(video)}")
    log(f"    length    {hms(dur)}")
    log(f"    frame     {frame[0]}x{frame[1]}  {fps} fps"
        + ("" if not prescale else
           f"   (thu nho ve {C.REF[0]}x{C.REF[1]} de do toa do;"
           f" video ra van {frame[0]}x{frame[1]})"))
    log(f"    output    {os.path.basename(out)}" + ("  (dry run: not written)"
                                                    if dry_run else ""))
    log(f"    estimate  about {int((signal_s + screens_s + render_s) / 60)} min"
        f"   (analysis ~{int((signal_s + screens_s) / 60)} min"
        + ("" if dry_run else f", render ~{int(render_s / 60)} min") + ")")
    started = time.time()

    def stage(text):
        """Stage headings carry the running total: a long step should look
        like a long step, not like a hang."""
        log(f"  [{hms(time.time() - started)}] {text}")

    cache = os.path.join(workdir, "signal.npz")
    sig = _load_signal(cache, prescale) if reuse_signal else None
    if sig is None:
        stage("[1/4] clock + seat signal")
        sig = signal_mod.extract(video, dur, workers, progress=log,
                                 prescale=prescale)
        np.savez_compressed(cache, sig=sig,
                            fingerprint=_signal_fingerprint(prescale))
    else:
        stage(f"[1/4] clock + seat signal (reusing cached signal)")
    t, widget, seat, mine, theirs = signal_mod.interpret(sig)
    # The unknown share belongs in here. Reporting only the two seats read as
    # "100% left" on a stream whose first hour was never named at all, which is
    # the difference between a measurement and a default -- and on that stream
    # the default was wrong for three games.
    log(f"        seat: blue/right {100*(seat>0).mean():.0f}%   "
        f"red/left {100*(seat<0).mean():.0f}%   "
        f"unknown {100*(seat==0).mean():.0f}% (kept, not attributed)")
    # Report what the two clock lines actually look like. The bare "overlay not
    # found" warning this replaces was read as a fact about the video, when the
    # cause was the detector measuring the wrong colour on each line -- so say
    # which colour each line came out as, and let the number be checkable.
    ink_up = sig[:, signal_mod.IDX["n_up"]]
    ink_lo = sig[:, signal_mod.IDX["n_lo"]]
    hue_up = sig[:, signal_mod.IDX["c_up"]]
    hue_lo = sig[:, signal_mod.IDX["c_lo"]]
    lit = (ink_up > C.P_DIGIT) | (ink_lo > C.P_DIGIT)
    if lit.any():
        red_upper = 100 * (hue_up[lit] > hue_lo[lit]).mean()
        log(f"        clock lines: upper reads red in {red_upper:.0f}% of "
            f"samples with digits, blue in {100 - red_upper:.0f}%")
    log(f"        H2H clock overlay present in {100 * widget.mean():.0f}% of samples")
    if widget.mean() < 0.2:
        log("        WARNING: both clock lines were readable in under 20% of "
            "samples, so almost nothing can be proved idle and little will be "
            "cut. Check a few timestamps with "
            "tools/inspect_frames.py clock <video> <t> -- if it prints digits "
            "there, the CLK coordinates in tlh/config.py are off for this VOD.")

    cand, both_frozen = seg_mod.candidate_spans(t, widget, mine, theirs)
    stage("[2/4] lobby / menu / reconnect screens")
    dead_t = screens.dead_screens(video, cand, workers, progress=log,
                                  prescale=prescale)
    stage("[3/4] map vs combat while both clocks are frozen")
    map_t = screens.map_showing(video, both_frozen, workers, progress=log,
                                prescale=prescale)

    segs, stats = seg_mod.build(t, widget, mine, theirs, dead_t, map_t, dur)
    kept = sum(b - a for a, b in segs)
    log(f"\n  segments {len(segs)}    kept {hms(kept)} ({100*kept/dur:.1f}%)    "
        f"removed {hms(dur - kept)}")
    for name, secs in stats.items():
        log(f"      {name:<24} {hms(secs)}")

    csv_path = os.path.join(workdir, "segments.csv")
    with open(csv_path, "w") as fh:
        fh.write("idx,start_s,end_s,dur_s,start_hms,end_hms\n")
        for k, (a, b) in enumerate(segs, 1):
            fh.write(f"{k},{a:.2f},{b:.2f},{b-a:.2f},{hms(a)},{hms(b)}\n")
    # Closed explicitly. Left to the garbage collector this relied on CPython
    # freeing the handle promptly to flush it -- true in practice, but the
    # failure if it is ever not true is a truncated segments.json, which the
    # next run reads back as a valid shorter cut.
    with open(os.path.join(workdir, "segments.json"), "w") as fh:
        json.dump(segs, fh)
    log(f"  segment list -> {csv_path}")

    chapters = timeline.build(sig, segs)
    chap_path = os.path.join(workdir, "chapters.txt")
    timeline.write_youtube(chapters, chap_path)
    # Also beside the video, named to match it, since that is where anyone
    # looking for it will look.
    # parts_only writes no output file, so there is nowhere beside it to put
    # these -- the copy in workdir is the only one that makes sense.
    if not dry_run and not parts_only and not per_game:
        beside = naming.chapters_path(out)
        os.makedirs(os.path.dirname(beside), exist_ok=True)
        timeline.write_youtube(chapters, beside)
        chap_path = beside
    log(f"  {len(chapters)} chapters -> {chap_path}")
    log(f"  analysis took {(time.time()-started)/60:.1f} min")

    if dry_run:
        log("  dry run: stopping before render")
        return 0
    if not segs:
        log("  nothing to keep, no output written")
        return 1

    # Found once, before any piece is encoded, so every piece gets the SAME
    # rectangle. Per-piece detection would let one piece miss and publish the
    # code on its own.
    cover = None
    if C.QR_COVER.exists():
        cover = (C.QR_COVER,) + qrcover.find(video, dur, frame,
                                            progress=log)
    else:
        log(f"        no cover image at {C.QR_COVER}, QR left visible")

    if per_game:
        return _render_per_game(video, segs, sig, out, workdir, render_workers,
                                keep_parts, started, stage, log, cover, fps,
                                min_game)

    partsdir = os.path.join(workdir, "parts")
    stage(f"[4/4] render -> {partsdir if parts_only else out}")
    rc = render_mod.run(video, segs, out, render_workers,
                        outdir=partsdir, progress=log,
                        keep_parts=keep_parts or parts_only,
                        parts_only=parts_only, cover=cover, fps=fps)
    if rc == 0 and parts_only:
        log(f"  done  pieces in {partsdir}   "
            f"{(time.time()-started)/60:.1f} min total")
    elif rc == 0:
        total = kept + C.BLACK * (len(segs) - 1)
        log(f"  done  {out}   {os.path.getsize(out)/2**30:.2f} GiB   "
            f"{hms(total)}   {(time.time()-started)/60:.1f} min total")
    return rc


def _render_per_game(video, segs, sig, out, workdir, render_workers,
                     keep_parts, started, stage, log, cover=None, fps="30",
                     min_game=0.0):
    """One video per game, instead of one video for the whole stream.

    The games come from timeline.played_games, so a file called "(game 3)"
    holds the same game the chapter labels call game 3. Each game gets its own
    chapter file too: timeline.build measures against whatever segment list it
    is given, so passing one game's segments rebases its chapters to that
    video's own 00:00.

    `min_game` (seconds, 0 for off) drops games too short to be worth a video
    -- a biome death or an early concede. Applied HERE and not inside
    played_games, which would be the obvious place and is the wrong one:
    timeline.build() numbers its chapter labels off that same list, so
    filtering it would renumber every later game. Dropping game 3 would leave
    the fourth game of the stream called "game 3" in both its filename and its
    chapters, and nothing would say the third had ever existed. Skipping at
    the render step keeps the numbering honest and says what it skipped.
    """
    games = timeline.played_games(sig)
    if not games:
        log("  no game long enough to be worth its own video "
            f"(under {int(timeline.MIN_GAME)}s counts as a map re-roll)")
        return 1

    stage(f"[4/4] render {len(games)} game(s), one video each")

    # Footage kept by the cut but lying between two games -- a map re-roll, or
    # lobby time that survived -- belongs to no game and lands in none of these
    # videos. Measured on one VOD that was 10:10 of 2:35:13, so it gets said
    # out loud rather than quietly dropped.
    covered = sum(sum(b - a for a, b in seg_mod.within(segs, g[1], g[2]))
                  for g in games)
    outside = sum(b - a for a, b in segs) - covered
    if outside > 30:
        log(f"    {hms(outside)} of kept footage falls between games and is in "
            f"none of these videos (use one video for the whole stream to keep it)")

    failed, made, short = [], [], []
    for number, g_start, g_end, _runs in games:
        span = g_end - g_start
        if min_game and span < min_game:
            # Said out loud with both numbers, because the threshold is a
            # preference and this is the line that tells someone it was set
            # too high -- a game dropped in silence is one nobody knows to go
            # back for.
            short.append((number, span))
            log(f"    game {number}  {hms(span)} in the source, under the "
                f"{hms(min_game)} minimum -- not rendered")
            continue
        part = seg_mod.within(segs, g_start, g_end)
        if not part:
            log(f"    game {number}: nothing kept here, skipped")
            continue
        target = naming.game_output_name(out, number)
        kept = sum(b - a for a, b in part)
        log(f"    game {number}  {hms(kept)} in {len(part)} segment(s) "
            f"-> {os.path.basename(target)}")
        # A stream that switches to a different game mid-way leaves no day
        # counter for the length of it, and if the counter resumes legally
        # afterwards this span swallows it. Not cut -- the rule keeps what it
        # cannot identify -- but said out loud, because the video then holds
        # something that is not Heroes.
        blind = timeline.counter_gap(sig, g_start, g_end)
        if blind >= timeline.MIN_GAME:
            log(f"      {hms(blind)} of this span shows no day counter at all; "
                f"if the stream switched to another game, it is in this video")
        timeline.write_youtube(timeline.build(sig, part),
                               naming.chapters_path(target))
        rc = render_mod.run(
            video, part, target, render_workers,
            outdir=os.path.join(workdir, f"parts-game{number}"),
            progress=log, keep_parts=keep_parts, cover=cover, fps=fps)
        if rc:
            failed.append(number)
        else:
            made.append((target, kept))

    for target, kept in made:
        size = os.path.getsize(target) / 2 ** 30 if os.path.exists(target) else 0
        log(f"  done  {target}   {size:.2f} GiB   {hms(kept)}")
    log(f"  {len(made)} video(s) in {(time.time() - started) / 60:.1f} min total")
    if short:
        saved = sum(span for _n, span in short)
        log(f"  {len(short)} game(s) under the {hms(min_game)} minimum, "
            f"{hms(saved)} of source not rendered: "
            + ", ".join(f"game {n} ({hms(s)})" for n, s in short))
        log("  lower the minimum on the Cài đặt tab to render them")
    if failed:
        log(f"  game(s) that failed to render: {failed}")
    return 1 if failed else 0
