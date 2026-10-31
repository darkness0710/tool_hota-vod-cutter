"""Encode each kept segment with its transition, then join them.

Each segment is encoded separately with a fade in, a fade out, and 0.4 s of
black appended by `tpad`/`apad`. Baking the black hold into the segment itself
means every file in the concat list comes out of the same encoder with the same
parameters, so the final join is a stream copy and cannot drift.

Cutting per segment is also faster than one filter pass over the whole VOD: a
segment only decodes its own range instead of the entire file.

Audio is faded alongside the video. Without `afade` every join pops, because
the cut lands mid-sentence in the streamer's commentary.
"""
import os
import shutil
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from . import config as C
from . import encoder
from . import insert as insert_mod
from .ffmpeg import FF, audio_layout, has_audio


def _clip(job):
    """Encode one spliced-in clip so it joins the pieces around it.

    The concat at the end is a stream copy, which only works when every piece
    agrees on size, frame rate, pixel format and audio layout. The clip is
    whatever the streamer recorded -- 60 fps out of OBS, portrait off a phone,
    with or without sound -- so it is brought to the VOD's own numbers here:
    fitted inside the frame and padded with black rather than stretched, at
    the VOD's rate, in the VOD's channel layout, and given a silent track if
    it has none. The layout is not a detail: a stereo clip joined into a mono
    VOD came out as a file that called itself mono throughout and played the
    clip's audio wrong.

    The same fade in, fade out and black hold as a segment, so the clip looks
    like a cut in the video rather than something pasted into it.
    """
    clip, secs, i, is_last, outdir, codec, qflag, fps, size, layout = job
    out = os.path.join(outdir, f"seg{i:04d}.mp4")
    fade_out_at = max(0.0, secs - C.FADE)
    vf = ""
    if size:
        w, h = size
        vf = (f"scale={w}:{h}:force_original_aspect_ratio=decrease,"
              f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:color=black,")
    vf += (f"setsar=1,format=yuv420p,"
           f"fade=t=in:st=0:d={C.FADE},"
           f"fade=t=out:st={fade_out_at:.3f}:d={C.FADE}")
    af = (f"aresample=44100,aformat=channel_layouts={layout},"
          f"afade=t=in:st=0:d={C.FADE},"
          f"afade=t=out:st={fade_out_at:.3f}:d={C.FADE}")
    if not is_last:
        vf += f",tpad=stop_mode=add:stop_duration={C.BLACK}:color=black"
        af += f",apad=pad_dur={C.BLACK}"
    cmd = [FF, "-v", "error", "-i", str(clip)]
    if has_audio(str(clip)):
        cmd += ["-filter_complex", f"[0:v]{vf}[v];[0:a]{af}[aout]"]
    else:
        cmd += ["-f", "lavfi", "-t", f"{secs:.3f}",
                "-i", f"anullsrc=r=44100:cl={layout}",
                "-filter_complex", f"[0:v]{vf}[v];[1:a]{af}[aout]"]
    cmd += ["-map", "[v]", "-map", "[aout]",
            "-c:v", codec] + encoder.quality_args(qflag) + [
        "-r", fps, "-fps_mode", "cfr",
        "-c:a", "aac", "-b:a", "160k", "-ar", "44100", "-y", out]
    rc = subprocess.call(cmd, stdout=subprocess.DEVNULL,
                         stderr=subprocess.STDOUT)
    return i, rc


def _one(job):
    if job[0] == "clip":
        return _clip(job[1:])
    video, i, a, b, is_last, outdir, codec, qflag, cover, fps = job
    dur = b - a
    out = os.path.join(outdir, f"seg{i:04d}.mp4")
    fade_out_at = max(0.0, dur - C.FADE)
    vf = (f"fade=t=in:st=0:d={C.FADE},"
          f"fade=t=out:st={fade_out_at:.3f}:d={C.FADE}")
    af = (f"afade=t=in:st=0:d={C.FADE},"
          f"afade=t=out:st={fade_out_at:.3f}:d={C.FADE}")
    if not is_last:
        vf += f",tpad=stop_mode=add:stop_duration={C.BLACK}:color=black"
        af += f",apad=pad_dur={C.BLACK}"
    cmd = [FF, "-v", "error", "-ss", f"{a:.3f}", "-t", f"{dur:.3f}",
           "-i", video]
    if cover is None:
        cmd += ["-vf", vf, "-af", af]
    else:
        # The cover rides in the encode each segment already does, so it costs
        # no extra decode pass -- one composite per frame against a re-encode
        # that was happening anyway.
        path, cx, cy, cw, chh = cover
        cmd += ["-i", str(path)]
        # force_original_aspect_ratio=increase + crop is a FILL, not a fit: the
        # logo is square and the card is not, and a fit would letterbox the
        # difference, leaving strips of the QR showing along two edges. Filling
        # crops the logo instead, which costs a band off the top and bottom of
        # a graphic nobody reads closely.
        #
        # eof_action=repeat because the overlay input is a still: it delivers
        # one frame and ends, and the default would drop the cover from the
        # second frame onward. Left implicit this is the failure that renders
        # a single covered frame and then hours of exposed QR.
        cmd += ["-filter_complex",
                f"[1:v]scale={cw}:{chh}:force_original_aspect_ratio=increase,"
                f"crop={cw}:{chh}[cov];"
                f"[0:v][cov]overlay={cx}:{cy}:eof_action=repeat[ov];"
                f"[ov]{vf},format=yuv420p[v];"
                f"[0:a]{af}[aout]",
                "-map", "[v]", "-map", "[aout]"]
    # -r/-fps_mode are not optional: h264_qsv refuses to open when the frame
    # rate is not constant, and the filter chain leaves it unset.
    #
    # The rate is the SOURCE's, not a fixed 60. Hard-coding 60 against a 30 fps
    # VOD -- which is what YouTube serves for this channel -- made ffmpeg
    # duplicate every frame: twice the frames to encode, a bigger file, and not
    # one extra moment of motion in it, because the second copy of a frame
    # carries nothing the first did not.
    cmd += ["-c:v", codec] + encoder.quality_args(qflag) + [
        "-r", fps, "-fps_mode", "cfr",
        "-c:a", "aac", "-b:a", "160k", "-ar", "44100", "-y", out]
    rc = subprocess.call(cmd, stdout=subprocess.DEVNULL,
                         stderr=subprocess.STDOUT)
    return i, rc


def run(video, segments, out, workers=3, outdir="parts", progress=print,
        keep_parts=False, parts_only=False, cover=None, fps="60",
        inserts=(), size=None):
    """Render `segments` of `video` into `out`. Returns an exit code.

    `cover` is (image, x, y, w, h) painted over every frame, or None.
    `fps` is the source's own rate, as a string ffmpeg -r accepts.
    `inserts` are clips to splice in, as tlh/insert.py plans them, and `size`
    the source's (w, h) they are fitted to. The QR cover is not painted on a
    clip: it is the streamer's own recording, with no donation code in it.

    `parts_only` stops once the pieces are written, without concatenating
    them. When the question is what the detector decided, the pieces ARE the
    answer -- one file per kept stretch, watchable on their own -- and the
    finished file is a second copy of the same footage.
    """
    os.makedirs(outdir, exist_ok=True)
    codec, qflag = encoder.detect(log=progress)
    pieces = insert_mod.plan(segments, inserts)
    layout = (audio_layout(video) or "stereo") if inserts else None
    jobs = []
    for i, piece in enumerate(pieces):
        is_last = i == len(pieces) - 1
        if piece[0] == "clip":
            jobs.append(("clip", piece[1], piece[2], i, is_last, outdir,
                         codec, qflag, fps, size, layout))
        else:
            jobs.append((video, i, piece[1], piece[2], is_last, outdir,
                         codec, qflag, cover, fps))

    done, started, failed = 0, time.time(), []
    with ThreadPoolExecutor(workers) as pool:
        # as_completed, not map: map yields strictly in order, so one long
        # early segment holds back the count for every short one that has
        # already finished, and the progress line reports a third of the real
        # figure with a wildly pessimistic eta.
        futures = [pool.submit(_one, job) for job in jobs]
        for future in as_completed(futures):
            i, rc = future.result()
            done += 1
            if rc:
                failed.append(i)
                progress(f"    segment {i} failed rc={rc}")
            # Every fifth piece was a line every one to two minutes, which
            # left a progress bar reading 0% while nine of twenty-eight were
            # already rendered. One line per piece is only noise on a VOD with
            # a hundred of them.
            step = 1 if len(jobs) <= 40 else 5
            if done % step == 0 or done == len(jobs):
                el = time.time() - started
                progress(f"    {done}/{len(jobs)}  {el/60:.1f}min elapsed  "
                         f"eta {el/done*(len(jobs)-done)/60:.1f}min")

    if failed:
        progress(f"    {len(failed)} segment(s) failed, not concatenating: {failed}")
        # Discard the pieces. Nothing can be salvaged from them: _one always
        # re-encodes with -y and never skips a piece that is already there, so
        # a retry rebuilds every one of them and these files are read by
        # nothing, ever again. Leaving them was a permanent leak, because the
        # SUCCESS path below is the only thing that removes this directory --
        # measured after a Ctrl+C killed one piece of a 23-piece game, 1.1 GiB
        # sat stranded in work/ with no way to reclaim it except Clear.cmd's
        # work group, which took the signal cache with it.
        #
        # Note what a killed piece looks like before trusting one: seg0020 of
        # that run was a 73 MiB file where a whole segment is 229 MiB, i.e. a
        # plausible-looking truncation. So resuming from surviving pieces
        # would have to check every piece's DURATION, not just that it exists.
        if not (keep_parts or parts_only):
            stranded = sum(os.path.getsize(os.path.join(outdir, n))
                           for n in os.listdir(outdir))
            shutil.rmtree(outdir, ignore_errors=True)
            progress(f"    discarded {stranded/2**30:.2f} GiB of unusable "
                     f"pieces (a retry re-renders them all anyway)")
        return 1

    if parts_only:
        files = sorted(n for n in os.listdir(outdir) if n.endswith(".mp4"))
        total = sum(os.path.getsize(os.path.join(outdir, n)) for n in files)
        progress(f"    {len(files)} piece(s), {total/2**30:.2f} GiB, kept in "
                 f"{outdir}")
        progress("    parts only: not concatenating")
        return 0

    listing = os.path.join(outdir, "concat.txt")
    with open(listing, "w") as fh:
        for i in range(len(pieces)):
            fh.write(f"file 'seg{i:04d}.mp4'\n")
    rc = subprocess.call(
        [FF, "-v", "error", "-f", "concat", "-safe", "0", "-i", listing,
         "-c", "copy", "-movflags", "+faststart", "-y", out])

    if rc == 0 and keep_parts is False:
        # The pieces are now a duplicate of the finished file -- for an eight
        # hour VOD that is several gigabytes sitting there for nothing. The
        # expensive thing to recompute is the signal, and that is cached
        # separately.
        freed = sum(os.path.getsize(os.path.join(outdir, n))
                    for n in os.listdir(outdir))
        shutil.rmtree(outdir, ignore_errors=True)
        progress(f"    cleaned up {freed/2**30:.2f} GiB of rendered pieces")
    return rc
