"""Splice a short clip of the streamer's own -- a "like and subscribe" -- into
each per-game video.

Two kinds of anchor, both read off things the chapter list already knows:

* **before a hero-vs-hero battle** -- every one of them, a couple of seconds
  before the battle screen opens. The viewer is waiting for the fight, so a
  ten-second ask there is one they sit through.
* **a day rolling over** -- a random choice among the game's day changes,
  never the first day (the game has barely started) nor the last (the result
  is about to land).

Anchors are kept at least `gap_days` in-game days apart, and battles are
placed first: they are the fixed ones, the day changes fill what is left.
The random choice is seeded by the video's name and the game number, so
rendering the same VOD again puts the clip in the same places.

Per-game videos only. A whole-stream video spans several games whose day
counters each restart at 1, so "two days apart" stops meaning anything there,
and the person this was built for posts one video per game anyway.

Nothing here touches a frame: `choose()` decides WHERE, `plan()` turns that
into the ordered list of pieces render.py encodes and timeline.py measures.
Both of them read the same plan, which is what keeps the chapter list in step
with the video it describes.
"""
import random
import zlib

from . import config as C

COMBAT_LEAD = 2.0   # seconds before the battle screen; the walk-up stays in
MIN_SPLIT = 1.5     # a kept stretch is not split into a piece shorter than this
MIN_APART = 60.0    # seconds of source between two clips, whatever the days say
SNAP = 30.0         # how far past an anchor to look for kept footage


def day_number(value):
    """(month, week, day) -> days since the game began, 1-based."""
    month, week, day = value
    return (month - 1) * 28 + (week - 1) * 7 + day


def _snap(t, segments, limit):
    """First kept moment in [t, limit], or None.

    A day can roll over while the opponent's turn is on screen, which the cut
    has removed. The clip then goes where the viewer first SEES the new day:
    the start of the next kept stretch, as long as that is still the same day.
    """
    for a, b in segments:
        if a <= t < b:
            return t
        if t < a <= limit:
            return a
    return None


def _day_at(runs, t):
    """The day showing at source time `t`, or the last one before it."""
    current = None
    for value, start, _end in runs:
        if start > t:
            break
        current = value
    return current


def choose(segments, runs, battles, game_span, *, combat, days, gap_days,
           seed):
    """Where to put the clip in one game.

    Returns (anchors, note): `anchors` is a sorted list of (source_time, kind,
    day) with kind "combat" or "day"; `note` explains a shortfall, or is "".
    """
    g_start, g_end = game_span
    taken = []                                  # (t, kind, day)

    def fits(t, day):
        for other_t, _kind, other_day in taken:
            if abs(t - other_t) < MIN_APART:
                return False
            if day is not None and other_day is not None \
                    and abs(day - other_day) < gap_days:
                return False
        return True

    if combat:
        for b_start, b_end in battles:
            if not g_start <= b_start <= g_end:
                continue
            t = _snap(max(g_start, b_start - COMBAT_LEAD), segments, b_end)
            value = _day_at(runs, b_start)
            day = day_number(value) if value else None
            if t is not None and fits(t, day):
                taken.append((t, "combat", day))

    note = ""
    if days:
        pool = []
        # [1:-1]: not the first day, not the last one.
        for value, start, end in runs[1:-1]:
            t = _snap(start, segments, end)
            if t is not None:
                pool.append((t, day_number(value)))
        random.Random(seed).shuffle(pool)
        placed = 0
        for t, day in pool:
            if placed == days:
                break
            if fits(t, day):
                taken.append((t, "day", day))
                placed += 1
        if placed < days:
            note = (f"only {placed} day change(s) far enough apart"
                    if pool else "no day change between the first and last day")
    return sorted(taken), note


def seed_for(video, game):
    """Same video, same game -> same choice, run after run."""
    return zlib.crc32(f"{video}|{game}".encode("utf-8"))


def plan(segments, inserts):
    """Interleave kept stretches and clips, in playing order.

    `inserts` is [(source_time, clip_path, clip_seconds), ...]. Returns pieces
    ("seg", a, b) and ("clip", path, seconds). A stretch the clip lands inside
    is split in two; one whose edge it lands within MIN_SPLIT of is not, and
    the clip goes before or after it whole -- a half-second piece with a fade
    at both ends is a flicker, not footage.
    """
    todo = sorted(inserts, key=lambda x: x[0])
    pieces, k = [], 0
    for a, b in segments:
        cur, after = a, []
        while k < len(todo) and todo[k][0] < b:
            t, path, secs = todo[k]
            k += 1
            if t - cur < MIN_SPLIT:
                pieces.append(("clip", path, secs))
            elif b - t < MIN_SPLIT:
                after.append(("clip", path, secs))
            else:
                pieces.append(("seg", cur, t))
                pieces.append(("clip", path, secs))
                cur = t
        pieces.append(("seg", cur, b))
        pieces.extend(after)
    return pieces


def clip_starts(pieces):
    """Where each clip begins in the finished video, in seconds."""
    out, acc = [], 0.0
    for piece in pieces:
        if piece[0] == "clip":
            out.append(acc)
            acc += piece[2]
        else:
            acc += piece[2] - piece[1]
        acc += C.BLACK
    return out


def output_time(pieces):
    """Map a source timestamp onto the timeline of `pieces`, or None.

    Half-open stretches first: where a stretch was split at `t`, the moment
    `t` belongs AFTER the clip, so a chapter for the battle or the new day
    points at the battle or the new day rather than at the clip in front of
    it. The closed check after that keeps the very last frame mappable.
    """
    spans, acc = [], 0.0
    for piece in pieces:
        if piece[0] == "seg":
            spans.append((piece[1], piece[2], acc))
            acc += piece[2] - piece[1]
        else:
            acc += piece[2]
        acc += C.BLACK

    def convert(src):
        for a, b, offset in spans:
            if a <= src < b:
                return offset + (src - a)
        for a, b, offset in spans:
            if a <= src <= b:
                return offset + (src - a)
        return None
    return convert
