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
}

DEFAULTS = {name: spec["default"] for name, spec in FIELDS.items()}


def _clean(raw):
    """Known keys only, each an int inside its own range."""
    out = dict(DEFAULTS)
    if not isinstance(raw, dict):
        return out
    for name, spec in FIELDS.items():
        if name not in raw:
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
