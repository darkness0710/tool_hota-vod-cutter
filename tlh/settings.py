"""Preferences the person using the page can change, kept between runs.

Deliberately not part of tlh/config.py. That file holds the detector's
constants -- every one of them a measured number with a paragraph saying which
VOD it was measured on -- and it is edited by whoever is adapting the tool to a
different overlay. What lives here is the other kind of value: a preference
with no right answer, which the page offers as a box to type in.

Stored in the project root beside .encoder.json, NOT under work/. work/ is what
the Dọn buttons empty, and WORK_SPARE in tlh/web.py spares exactly one file --
a preference that disappears every time someone reclaims disk space is worse
than having no preference at all.
"""
import json
import os

from .config import ROOT

PATH = ROOT / "settings.json"

# One entry per setting. Keeping the bounds here rather than in the page means
# the server validates what it stores whatever sent it -- the page, a curl, or
# a hand-edited settings.json -- instead of trusting a number that only the
# browser checked.
FIELDS = {
    # How long a game has to last before it is worth its own video.
    #
    # Measured on the SOURCE span of the game -- first to last day-counter
    # reading -- not on the length of the cut video. A game's length is a fact
    # about the game; how much of it survives the cut is a fact about the
    # detector, and pointing this at the second one would move the threshold
    # every time the cut rule was tuned.
    #
    # 30 is what was asked for, on the grounds that a game shorter than that
    # ended with someone dying to the biome or conceding early. It is a box on
    # the page rather than a constant because that reasoning is about this
    # streamer's games, not about Heroes 3 -- and because it is wrong often
    # enough to want changing: on the one stream measured, 30 minutes also
    # dropped a game holding 24:39 of real play.
    #
    # 0 turns it off and renders every game.
    "min_game_minutes": {"default": 30, "min": 0, "max": 600},

    # How long a download may go COMPLETELY silent before the page stops it
    # and starts it again by itself. 0 switches the watchdog off and leaves
    # the Chay lai button as the only way back.
    #
    # Measured against `heard` in tlh/web.py -- the last byte of ANY output,
    # parsed or not -- and NOT against the progress readout. That distinction
    # is the whole reason a timer is safe here: the slow downloads this tool
    # exists to sit through are slow, not silent. One VOD's audio stream
    # crawled for 85 minutes at 53 KiB/s while printing a line every second,
    # and a watchdog that reads total silence never sees it.
    #
    # 30 because nothing healthy in a download is silent for half an hour:
    # aria2c redraws its readout every second and so does our own bar. The one
    # exception is the mux at the end, which says nothing for its whole length
    # -- that phase names itself (`quiet == "merge"`) and is given
    # STALL_MERGE_FACTOR times as long.
    #
    # Downloads only. A restart there resumes from the .part file and costs
    # seconds; restarting a render throws away up to an hour of encoding, and
    # how long one ffmpeg piece may legitimately run without printing is not
    # measured here. See WATCHED_STAGES in tlh/web.py.
    "stall_restart_minutes": {"default": 30, "min": 0, "max": 600},

    # The "like and subscribe" clip spliced into each per-game video; see
    # tlh/insert.py. Off until someone turns it on: it changes every video
    # that comes out, which nobody should discover after uploading one.
    #
    # Switches are ints, 0 or 1, so every field still has one shape and one
    # range check -- a JSON true would arrive as 1 anyway.
    "insert_on": {"default": 0, "min": 0, "max": 1},
    # Which file in insert/: a bare name, "" for the first one there, or
    # RANDOM for a different pick per game. Only the name is stored; whether
    # it still exists is checked when a run starts, because the folder is
    # filled by hand.
    "insert_file": {"default": "", "kind": "name"},
    "insert_day_on": {"default": 1, "min": 0, "max": 1},
    # How many day changes per game get the clip. Ten is far past anything a
    # viewer would sit through; the cap is there to stop a typo, not a taste.
    "insert_days": {"default": 1, "min": 1, "max": 10},
    "insert_combat": {"default": 1, "min": 0, "max": 1},
    # In-game days between two clips, battles included.
    "insert_gap_days": {"default": 2, "min": 0, "max": 30},
}

RANDOM = "*"            # not a legal Windows filename, so never a real one

DEFAULTS = {name: spec["default"] for name, spec in FIELDS.items()}


def _clean(raw):
    """Known keys only, each an int inside its own range or a bare name."""
    out = dict(DEFAULTS)
    if not isinstance(raw, dict):
        return out
    for name, spec in FIELDS.items():
        if name not in raw:
            continue
        if spec.get("kind") == "name":
            # A bare file name or nothing: no separator, so a hand-edited
            # settings.json cannot point a run at a file outside insert/.
            value = raw[name] if isinstance(raw[name], str) else ""
            value = value.strip()
            ok = value == RANDOM or (
                os.path.basename(value) == value and "/" not in value
                and ".." not in value)
            out[name] = value if ok else spec["default"]
            continue
        try:
            value = int(raw[name])
        except (TypeError, ValueError):
            continue                    # keep the default rather than crash
        out[name] = max(spec["min"], min(spec["max"], value))
    return out


def load():
    """Current settings, with defaults filled in. Never raises."""
    try:
        with open(PATH, encoding="utf-8") as fh:
            return _clean(json.load(fh))
    except (OSError, ValueError):
        # Missing is the normal case on a fresh install; corrupt is rare and
        # not worth stopping a five-hour render over. Both mean "defaults".
        return dict(DEFAULTS)


def save(raw):
    """Validate, write, and return what was actually stored."""
    values = _clean(raw)
    tmp = PATH.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(values, fh, ensure_ascii=False, indent=2)
    tmp.replace(PATH)                   # atomic: the page may read at any time
    return values
