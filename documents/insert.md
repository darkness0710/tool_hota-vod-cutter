# The like & subscribe insert

A clip of the streamer's own -- ten seconds asking viewers to like and
subscribe -- spliced into every **per-game** video. Switched on in the
**Cài đặt** tab; off by default, because it changes every video that comes
out.

```
insert\like-sub.mp4          the clip, dropped in by hand
Cài đặt -> Chèn đoạn nhắc    on/off, which file, when, how far apart
```

## Where it goes

Two kinds of moment, both already known to the chapter list
([chapters.md](chapters.md)), so choosing them costs no extra analysis:

| tick | where | how many |
|---|---|---|
| **Trước combat PvP** | 2 s before every hero-vs-hero battle opens | every battle, placed first |
| **Qua ngày** | the moment a new day shows | N per game, picked at random |

Rules, in the order they are applied:

1. Battles first. They are the fixed ones; a battle closer than the gap to one
   already taken is skipped.
2. Day changes are drawn at random from what is left, **never the first day**
   (the game has barely started) **nor the last** (the result is about to
   land).
3. Every insert is at least `gap` in-game days from every other, battles
   included, and never under a minute of source apart whatever the days say.
4. Too few days for the count asked: as many as fit. The job card says
   `chèn 1/2 (chỉ 1 lần qua ngày đủ cách nhau)` rather than leaving it to be
   noticed.

The random draw is seeded by the file name and the game number, so rendering
the same VOD again puts the clip in the same places. With several files in
`insert\` and **Ngẫu nhiên mỗi ván** picked, each game gets one of them, by the
same seed.

A day can roll over while the opponent's turn is on screen, which the cut has
removed. The clip then goes where the viewer first *sees* the new day: the start
of the next kept stretch, as long as that is still the same day.

## Why per-game only

A whole-stream video spans several games, each restarting its day counter at 1,
so "two days apart" stops meaning anything; and the person this was built for
posts one video per game. The option on the page says so under its
description, and the line on the step-1 card reads "không áp dụng".

## How it is joined

The final join is a stream copy, which only works when every piece agrees on
size, frame rate, pixel format and audio layout. The clip is whatever was
recorded, so it is encoded once per place it goes, to the VOD's own numbers:

* fitted inside the frame and padded with black -- a portrait phone clip gets
  bars, not a stretch;
* the VOD's frame rate (a 60 fps OBS clip in a 30 fps VOD drops frames rather
  than doubling the VOD's);
* yuv420p, SAR 1;
* the VOD's **channel layout**. Measured against a mono source: a clip forced
  to stereo joined into a file that called itself mono throughout. Read from
  the source now, stereo if it cannot be;
* a silent track if the clip has none, so the join has audio to join.

It gets the same 0.3 s fades and 0.4 s black hold as every cut, so it reads as
a cut in the video rather than something pasted on top. Where it lands inside a
kept stretch, that stretch is split in two; within 1.5 s of an edge it is not,
and the clip goes before or after the stretch whole.

The QR cover is not painted on the clip: it is the streamer's recording, with no
donation code in it.

## The chapters move with it

`timeline.build()` measures against the same plan `render.py` encodes
(`insert.plan()`), so every chapter after a clip is pushed on by the clip's
length. A chapter at the exact moment of a clip -- the battle, the new day --
points **after** it, at the battle or the new day, not at the ask in front of
it.

## Checked

On synthetic sources (no VOD was on this machine): a 1080p30 source with mono
audio, a 1280x720 60 fps yuv444 clip with no audio, and a 720x1280 24 fps clip
with mono 22 kHz audio. The join decoded with no errors, 1878 frames for 62.6 s
at 30 fps, every clip at 1920x1080 with bars where expected, and the output's
length matched the plan to within 0.07 s.
