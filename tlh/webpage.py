"""The single page tlh/web.py serves.

Kept as one string in one module on purpose: no static folder to lose, no
asset paths to get wrong, and the server stays a file you can read in one go.

The labels are Vietnamese because this page exists for the people who are not
going to read a console -- the rest of the project talks English to whoever is
editing it. English is available at a switch; see tlh/i18n.py.

The Vietnamese also stays inline in the markup below, next to its data-t key,
so the page reads correctly before the script runs and if it never runs.
"""
import json
import re

from . import config as C
from . import i18n

_HTML = r"""<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>TieuLinh-Hota-Download-And-Cut-Video</title>
<style>
  /* The ground is darker than the cards now, not lighter. Everything used to
     sit within four points of lightness of everything else, so nothing read as
     a surface and nothing read as behind one -- the page came out as a single
     grey field with lines drawn on it. Dropping the background and lifting the
     cards is what makes a card look like a card, and it costs no contrast on
     the text, which is what --ink and --dim are for. */
  :root {
    --bg: #0f1115; --card: #171a20; --raised: #1e222a; --sunken: #0c0e12;
    --line: #262b34; --line-soft: #1f242c;
    --ink: #e9ecf1; --dim: #949cab;
    --accent: #5aa9e6; --accent-dim: #4b9cdd;
    --accent-soft: rgba(90, 169, 230, .13);
    --ok: #4caf82; --warn: #d9a13b; --bad: #d9534f;
  }
  * { box-sizing: border-box; }
  body { margin: 0; background: var(--bg); color: var(--ink);
         font: 14px/1.6 "Segoe UI", system-ui, sans-serif;
         -webkit-font-smoothing: antialiased; }
  .wrap { max-width: 1000px; margin: 0 auto; padding: 30px 20px 72px; }
  .head { display: flex; align-items: flex-start; gap: 16px;
          margin-bottom: 18px; }
  .head h1 { flex: 1; min-width: 0; }
  .langs { display: inline-flex; gap: 2px; padding: 3px; flex: none;
           background: var(--sunken); border: 1px solid var(--line);
           border-radius: 9px; }
  .langs button { padding: 4px 11px; font-size: 12px; font-weight: 700;
        background: none; border: 0; color: var(--dim); border-radius: 5px; }
  .langs button:hover { color: var(--ink); background: #191e26; }
  .langs button.on, .langs button.on:hover { color: #0d1117;
        background: var(--accent); }
  /* The version, where it can be read without opening anything. It used to
     live only inside the Version tab, which meant the one question this page
     could not answer at a glance was which build you were looking at. */
  .vertag { flex: none; align-self: center; padding: 5px 12px;
            background: var(--sunken); border: 1px solid var(--line);
            border-radius: 9px; color: var(--dim); font: inherit;
            font-size: 12px; font-weight: 700; cursor: pointer; }
  .vertag:hover { color: var(--accent); border-color: var(--accent); }
  h1 { font-size: 21px; margin: 0 0 2px; letter-spacing: -.01em; }
  h1 a { color: var(--accent); font-weight: 400; font-size: 15px;
         text-decoration: none; }
  h1 a:hover { text-decoration: underline; }
  /* A short accent rule to the left of each section label. The labels are
     small dim uppercase by design -- they should not compete with the content
     under them -- but on a page this long that left them with nothing to
     catch the eye, so scanning for "2 · CHỌN NGUỒN" meant reading. A 3 px bar
     is enough to find a section without raising the label's own weight. */
  h2 { font-size: 12px; text-transform: uppercase; letter-spacing: .13em;
       color: var(--dim); margin: 34px 0 12px; font-weight: 700;
       position: relative; padding-left: 13px; }
  h2::before { content: ""; position: absolute; left: 0; top: 50%;
       transform: translateY(-50%); width: 3px; height: 13px;
       border-radius: 2px; background: var(--accent); opacity: .75; }
  /* A hairline of light along the top edge and a soft shadow under it. That
     pair is what reads as "raised" on a dark ground -- a border alone reads as
     a drawn rectangle, which is what these were. */
  .card { background: var(--card); border: 1px solid var(--line);
          border-radius: 12px; padding: 18px 20px; margin-bottom: 12px;
          box-shadow: inset 0 1px 0 rgba(255, 255, 255, .035),
                      0 2px 14px rgba(0, 0, 0, .28); }
  .drive { display: flex; align-items: center; gap: 12px; font-size: 13px; }
  .drive .bar { flex: 1; height: 10px; background: var(--sunken);
        border-radius: 999px; box-shadow: inset 0 1px 2px rgba(0, 0, 0, .5);
                overflow: hidden; }
  .drive .bar i { display: block; height: 100%; border-radius: 999px;
        background: linear-gradient(90deg, var(--accent-dim), #7fc4f0);
        transition: width .3s ease; }
  .row { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }
  input[type=text] { flex: 1; min-width: 260px; background: var(--sunken);
       border: 1px solid var(--line); color: var(--ink); border-radius: 8px;
       padding: 10px 12px; font: inherit; }
  input[type=text]::placeholder { color: #6b7381; }
  select, button { background: var(--raised); color: var(--ink); font: inherit;
       border: 1px solid var(--line); border-radius: 8px; padding: 9px 14px;
       cursor: pointer;
       transition: background .12s ease, border-color .12s ease,
                   color .12s ease; }
  select:hover, button:hover { background: #252b34; border-color: #333a46; }
  /* One button on the page starts the work. It is the only one that is filled,
     and the glow is what separates it from the row of outlined buttons beside
     it without making them look disabled. */
  button.go { background: linear-gradient(180deg, #6fb6ea, var(--accent-dim));
              border-color: var(--accent-dim); color: #06121c;
              font-weight: 700;
              box-shadow: 0 2px 12px rgba(90, 169, 230, .28); }
  button.go:hover { background: linear-gradient(180deg, #7dbef0, #58a6e3);
                    border-color: #58a6e3; }
  /* Keyboard focus has to be visible; a tool run from the keyboard should not
     have to be driven by guesswork. */
  a:focus-visible, button:focus-visible, select:focus-visible,
  input:focus-visible { outline: 2px solid rgba(90, 169, 230, .55);
                        outline-offset: 2px; }
  input[type=text]:focus { border-color: var(--accent-dim); outline: none;
                           box-shadow: 0 0 0 3px rgba(90, 169, 230, .15); }
  button.small { padding: 6px 11px; font-size: 13px; }
  button.danger { border-color: #5a3436; color: #e08c88; }
  button.danger:hover { background: #3a2426; }
  .files { display: flex; flex-direction: column; gap: 6px; }
  .file { display: flex; align-items: center; gap: 10px; font-size: 13px; }
  .file .nm { flex: 1; overflow: hidden; text-overflow: ellipsis;
              white-space: nowrap; }
  .file .sz { color: var(--dim); font-variant-numeric: tabular-nums; }
  /* Chạy is what the row is for; Mở and Xoá only reveal or remove. Tinted
     rather than filled -- a row of solid blue buttons down the list would
     shout louder than the one real call to action at the top of the card. */
  .file button[data-run]:not(:disabled) { border-color: #35566e;
        color: #bcdcf5; }
  .file button[data-run]:not(:disabled):hover { background: #223447; }
  .job .head { display: flex; align-items: baseline; gap: 10px; }
  .job .t { flex: 1; font-weight: 600; overflow: hidden;
            text-overflow: ellipsis; white-space: nowrap; }
  .badge { font-size: 12px; padding: 2px 9px; border-radius: 20px;
           border: 1px solid var(--line); color: var(--dim);
           white-space: nowrap; }
  .badge.run { border-color: var(--accent); color: var(--accent); }
  .badge.done { border-color: var(--ok); color: var(--ok); }
  .badge.bad { border-color: var(--bad); color: var(--bad); }
  .prog { height: 6px; background: #0e1014; border-radius: 3px; margin: 10px 0 6px;
          overflow: hidden; }
  .prog i { display: block; height: 100%; background: var(--accent);
            transition: width .4s; }
  .when { color: var(--dim); font-size: 12px; margin-top: 2px;
          font-variant-numeric: tabular-nums; }
  .when b { color: var(--ink); font-weight: 600; }
  .meta { color: var(--dim); font-size: 13px; }
  .meta b { color: var(--ink); font-weight: 600; }
  /* No max-width. A measure was tried and it was the wrong tool here: these
     notes sit in a card sized by the 16:9 video player above them, so capping
     the text at a comfortable reading width left the right 40% of the card
     visibly empty, which reads as a broken layout rather than as a kind one.
     The list below is what actually fixes the wall of text -- each item is one
     short sentence, so the line length never has to carry a paragraph. */
  .note { margin-top: 6px; font-size: 13px; line-height: 1.6; }
  /* A note that carries more than one fact is a LIST, not a paragraph with
     breaks in it. Three facts run together read as one wall and get skipped;
     bulleted, each is a thing the eye can land on and leave. The bullet also
     does the work <br><br> could not: it survives the line height, and it
     says where one fact ends without needing a blank line to show it. */
  .note ul, .foot ul { margin: 6px 0 0; padding-left: 18px; }
  .note li, .foot li { margin: 0 0 5px; }
  .note li:last-child, .foot li:last-child { margin-bottom: 0; }
  .note li::marker, .foot li::marker { color: var(--line); }
  .note.warn { color: var(--warn); }
  .note.bad { color: var(--bad); }
  /* Baseline, not the grid default of stretch. A dd holding a button.small
     is taller than its label by that button's padding, so with stretch the
     label sat against the top of the row while the value sat a few pixels
     lower -- every row with a button read as misaligned, and the rows without
     one looked fine, which made it look like a rendering glitch rather than a
     rule. Baseline lines the two up by the thing the eye actually uses. */
  .kv { display: grid; grid-template-columns: 120px 1fr; gap: 2px 10px;
        align-items: baseline; margin-top: 8px; font-size: 13px; }
  .kv dt { color: var(--dim); }
  .kv dd { margin: 0; overflow-wrap: anywhere; }
  pre { background: #0e1014; border: 1px solid var(--line); border-radius: 6px;
        padding: 10px; max-height: 300px; overflow: auto; font-size: 12px;
        margin: 10px 0 0; white-space: pre-wrap; }
  .empty { color: var(--dim); font-size: 13px; }
  .opts { padding: 4px 6px; }
  .opt { display: flex; gap: 12px; align-items: flex-start; padding: 12px 12px;
         border-radius: 9px; cursor: pointer;
         transition: background .12s ease, box-shadow .12s ease; }
  .opt:hover { background: var(--raised); }
  /* The radio dot was the only thing saying which of the three was picked, and
     at 13 px on a grey field that is not enough -- the answer to "what will
     this do when I press the button" should be readable without hunting for a
     dot. :has() is what lets the LABEL respond to its own input; where it is
     unsupported the dot still works and nothing is lost. */
  .opt:has(input:checked) { background: var(--accent-soft);
         box-shadow: inset 0 0 0 1px rgba(90, 169, 230, .38); }
  .opt input { margin: 3px 0 0; accent-color: var(--accent); flex: none; }
  .opt b { display: block; font-weight: 600; }
  .opt i { display: block; color: var(--dim); font-style: normal;
           font-size: 13px; margin-top: 2px; }
  .opt em { font-style: normal; color: var(--dim); font-weight: 400;
            font-size: 12px; }
  /* Baseline, for the reason .kv needs it: the dd carries a button whose
     padding makes the row taller than the label beside it, and the grid
     default of stretch then pins the label to the top of that row while the
     value sits lower. Same defect, second grid -- fixing one and not the
     other is how it came back. */
  .paths { display: grid; grid-template-columns: max-content 1fr;
           gap: 4px 14px; align-items: baseline; font-size: 12px; }
  .paths dt { color: var(--dim); }
  .paths dd { margin: 0; font-family: ui-monospace, Consolas, monospace;
              overflow-wrap: anywhere; }
  .paths dd button { margin-left: 8px; vertical-align: 1px; }
  /* One row per folder: path on the left, what is in it on the right.
     It used to stack the path above its own numbers and paint the path in
     full-strength ink while the size stayed dim -- brightest on the thing the
     reader already knows, faintest on the thing they came to read. */
  /* Three columns, not two. The size and the buttons used to share one
     max-content column, so a row reading "6.71 GiB 3 file" pushed its buttons
     further left than a row reading "0 0 file" -- the buttons came out ragged
     while the file list right below them, which gives each part its own
     column, lined up. display:contents on the dd is what lets the size and
     the button group be items of THIS grid instead of a grid of their own;
     a nested grid aligns within a row and never across them. */
  .folders { font-size: 13px; display: grid; align-items: center;
             grid-template-columns: 1fr max-content max-content;
             gap: 8px 16px; }
  .folders dt { color: var(--dim); font-size: 12px; min-width: 0;
                overflow-wrap: anywhere;
                font-family: ui-monospace, Consolas, monospace; }
  .folders dd { margin: 0; display: contents; }
  .folders dd .sz { color: var(--ink); text-align: right;
                    font-variant-numeric: tabular-nums; }
  .folders dd .acts { display: flex; gap: 8px; align-items: center; }
  /* The one button that removes several folders at once sits apart from the
     per-folder rows, with its total beside it: the number is the point, so it
     is not allowed to be the thing the reader has to add up themselves. */
  .clearall { display: flex; align-items: center; gap: 10px; margin-top: 12px;
              padding-top: 12px; border-top: 1px solid var(--line);
              font-size: 13px; }
  .clearall .sz { color: var(--dim); font-variant-numeric: tabular-nums; }
  .sep { color: var(--dim); font-size: 13px; margin-bottom: 11px; }
  /* Spelled once, so the lines inside a card sit at the same inset and the
     same distance apart. */
  .paths, .folders, .sep, details.dev { border-top: 1px solid var(--line);
        margin-left: 0; margin-right: 0; margin-top: 14px; padding-top: 12px; }
  details.dev { margin-bottom: 2px; }
  /* The browser's own disclosure triangle, not a glyph of ours: a CSS
     escape here came out as a tofu box, and every font has this one. */
  details.dev > summary { cursor: pointer; color: var(--dim); font-size: 13px;
       padding: 10px 6px 10px 2px; user-select: none; }
  details.dev > summary:hover { color: var(--ink); }
  code { background: var(--sunken); border: 1px solid var(--line-soft);
         border-radius: 5px; padding: 1px 6px; font-size: 12px;
         color: #c8d0dc; }
  .modal { position: fixed; inset: 0; background: rgba(6, 8, 11, .78);
           display: flex; align-items: flex-start; justify-content: center;
           padding: 40px 16px; overflow: auto; z-index: 10; }
  /* display:flex above beats the browser's own [hidden] rule, which is why
     the sheet showed itself on load. Say it again, louder. */
  .modal[hidden] { display: none; }
  .sheet { background: var(--card); border: 1px solid var(--line);
           border-radius: 10px; width: 100%; max-width: 860px; }
  .sheet > .head { display: flex; gap: 10px; align-items: center;
        padding: 14px 16px; border-bottom: 1px solid var(--line);
        flex-wrap: wrap; position: sticky; top: 0; background: var(--card);
        border-radius: 10px 10px 0 0; }
  .sheet > .head .n { flex: 1; color: var(--dim); font-size: 13px; }
  .vid { display: flex; gap: 12px; padding: 12px 16px;
         border-bottom: 1px solid var(--line); align-items: flex-start; }
  .vid:last-child { border-bottom: 0; }
  .vid img { width: 160px; height: 90px; object-fit: cover; border-radius: 6px;
             background: #0e1014; flex: none; }
  .vid .body { flex: 1; min-width: 0; }
  .vid .t { font-weight: 600; overflow-wrap: anywhere; }
  .vid .m { color: var(--dim); font-size: 13px; margin-top: 3px; }
  .vid .acts { display: flex; gap: 6px; margin-top: 8px; flex-wrap: wrap; }
  .vid.live { opacity: .55; }
  button:disabled { opacity: .45; cursor: not-allowed; }
  /* Keyboard users had nothing: the browser default ring is close to
     invisible on this background. :focus-visible so a mouse click does
     not leave a ring behind it. */
  :focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
  /* This is the page's top-level choice, so it is drawn as a control rather
     than as two words with a thin line under one of them. inline-flex so the
     bar hugs the two tabs instead of running the width of the page. */
  .tabs { display: inline-flex; gap: 4px; margin: 26px 0 6px; padding: 5px;
          background: var(--sunken); border: 1px solid var(--line);
          border-radius: 12px; }
  .tabs button { background: none; border: 0; color: var(--dim); font: inherit;
        font-size: 15px; font-weight: 700; letter-spacing: .2px;
        cursor: pointer; padding: 10px 22px; border-radius: 8px;
        transition: background .12s ease, color .12s ease; }
  .tabs button:hover { color: var(--ink); background: #191e26; }
  /* Near-black on the accent blue: the filled tab has to read as selected
     from across the room, and dark ink on that blue is what carries. */
  .tabs button.on, .tabs button.on:hover { color: #0d1117;
        box-shadow: 0 2px 10px rgba(90, 169, 230, .3);
        background: var(--accent); box-shadow: 0 2px 10px rgba(90,169,230,.28); }
  video.prev { width: 100%; max-height: 62vh; background: #000; border-radius: 8px;
        border: 1px solid var(--line); margin: 10px 0 4px; display: block; }
  .marks { display: flex; gap: 8px; align-items: center; flex-wrap: wrap;
           margin-top: 14px; }
  .marks.act { margin-top: 18px; }
  .marks label { color: var(--dim); font-size: 13px; }
  /* min-width and flex, not just width: the shared input[type=text] rule sets
     flex:1 and min-width:260px, and min-width beats width -- which stretched
     these two marks past the card and pushed the last button onto a line of
     its own. */
  .marks input { width: 108px; min-width: 0; flex: none; text-align: center;
                 font-family: ui-monospace, Consolas, monospace; }
  .marks .gap { flex: 1; min-width: 20px; }
  /* The controls under a paragraph need air; .row carries none of its own. */
  #tab-trim .row, #tab-qr .row { margin-top: 14px; }
  .kv dd a.mail { color: var(--accent); text-decoration: none; }
  .kv dd a.mail:hover { text-decoration: underline; }
  /* ONE grid for every release, not a block per release. The version labels
     have to line up down a column and the notes beside them have to start on
     the same x, and only a shared grid does that -- a block per release aligns
     within itself and never across, which is how the folder rows came out
     ragged.
     align-items: start, NOT baseline, and that is the whole trick here. The
     separator between releases is a border-top on both items of a row, so the
     two halves of that line have to begin at the same y. Baseline aligns the
     TEXT and lets the boxes start wherever they must to achieve it, which put
     the two halves a couple of pixels apart and drew a visibly stepped rule.
     start aligns the boxes, and a shared line-height then lines the text up
     anyway. */
  .rel { display: grid; grid-template-columns: max-content 1fr;
         gap: 0; align-items: start; margin-top: 8px; font-size: 13px;
         line-height: 1.6; }
  .rel dt { white-space: nowrap; font-variant-numeric: tabular-nums;
            padding-right: 18px; padding-left: 11px; line-height: 1.6;
            border-left: 3px solid transparent; }
  /* The current release, marked on the ROW rather than by the pill alone.
     A pill is a label you have to read; a tinted band with a bar down its
     edge is one you see before reading anything, which is the whole job of
     this tab. A tinted band across the row was tried and taken back out: at
     this size it read as a selected row in a table, as though it were
     something to act on. The bar and the colour on the number say the same
     thing without that.
     The transparent border sits on every dt so the text does not shift by
     three pixels between the current row and the rest. */
  .rel dt.now { border-left-color: var(--accent); }
  .rel dt.now b { color: var(--accent); }
  .rel dt b { color: var(--ink); font-size: 16px; font-weight: 600; }
  /* A quiet pill, not a filled one: it labels a row, it is not a control, and
     at the weight of a button it would read as something to press. */
  /* Filled, not outlined. Beside an accent-coloured version number an
     outlined pill of the same colour reads as part of the number; filled, it
     reads as a badge on it. Near-black text for the same reason the selected
     tab uses it -- accent blue is too light to carry white. */
  .rel dt .tag { display: inline-block; margin-left: 6px; padding: 1px 8px;
                 background: var(--accent); border-radius: 999px;
                 color: #0d1117; font-size: 11px; font-weight: 600;
                 vertical-align: 2px; }
  .rel dd { margin: 0; color: var(--dim); }
  .rel dd ul { margin: 0; padding-left: 18px; }
  .rel dd li { margin: 0 0 5px; }
  .rel dd li:last-child { margin-bottom: 0; }
  .rel dd li::marker { color: var(--line); }
  /* Each release is separated by a rule, because two stacked lists of bullets
     do not say on their own where one version ends and the next begins.
     The rule has to cross BOTH columns unbroken, which is why the grid has no
     column gap: 18px of gap showed straight through the border as a notch in
     the middle of the line. That spacing is padding on the dt instead, where
     it cannot interrupt anything. */
  .rel dt:not(:first-of-type), .rel dd:not(:first-of-type) {
      border-top: 1px solid var(--line); padding-top: 14px; }
  .rel dt, .rel dd { padding-bottom: 14px; }
  .rel dt:last-of-type, .rel dd:last-of-type { padding-bottom: 0; }
  .foot { color: var(--dim); font-size: 12px; margin-top: 26px;
          border-top: 1px solid var(--line); padding-top: 12px;
          line-height: 1.6; }
</style>
</head>
<body>
<div class="wrap">
  <div class="head">
    <h1><span data-t="head.title">Cắt VOD stream từ kênh</span>
      <a href="https://www.youtube.com/@TieulinhHOTA" target="_blank" rel="noreferrer">https://www.youtube.com/@TieulinhHOTA</a></h1>
    <button class="vertag" data-gotab="ver" data-tt="tip.version"
      title="Xem có gì mới trong bản này">v__VERSION__</button>
    <div class="langs" data-tt="lang.tip" title="Đổi ngôn ngữ giao diện">
      <button data-lang="vi" class="on">VI</button>
      <button data-lang="en">EN</button>
    </div>
  </div>

  <div class="card">
    <div class="drive">
      <span id="dv">&nbsp;</span>
      <span class="bar"><i id="dvbar" style="width:0"></i></span>
      <span id="dvfree" class="sz"></span>
    </div>
    <dl class="folders">
      <dt class="p-in">input\</dt>
      <dd><span id="szin" class="sz">&mdash;</span><span class="acts">
        <button class="small" data-open="input" data-t="btn.open"
          data-tt="tip.openFolder"
          title="Mở thư mục này trong Explorer">Mở</button>
        <button class="small danger" data-clear="input" data-t="btn.clear"
          data-tt="tip.clearFolder"
          title="Chuyển mọi file trong thư mục này vào Thùng rác">Dọn</button></span></dd>
      <dt class="p-out">output\</dt>
      <dd><span id="szout" class="sz">&mdash;</span><span class="acts">
        <button class="small" data-open="output" data-t="btn.open"
          data-tt="tip.openFolder"
          title="Mở thư mục này trong Explorer">Mở</button>
        <button class="small danger" data-clear="output" data-t="btn.clear"
          data-tt="tip.clearFolder"
          title="Chuyển mọi file trong thư mục này vào Thùng rác">Dọn</button></span></dd>
      <!-- work\ is listed for one reason: it was the only folder holding
           gigabytes that this page never mentioned, so a failed render's
           leftovers could not be seen OR removed from here. -->
      <dt class="p-work">work\</dt>
      <dd><span id="szwork" class="sz">&mdash;</span><span class="acts">
        <button class="small" data-open="work" data-t="btn.open"
          data-tt="tip.openWork"
          title="Mở thư mục work trong Explorer">Mở</button>
        <button class="small danger" data-clear="work" data-t="btn.clear"
          data-tt="tip.clearWork"
          title="Chuyển file tạm và cache phân tích vào Thùng rác">Dọn</button></span></dd>
    </dl>
    <div class="clearall">
      <button class="small danger" data-clear="all" data-t="btn.clearAll"
        data-tt="tip.clearAll"
        title="Chuyển input + output + work (kèm cache) vào Thùng rác">Dọn tất cả</button>
      <span id="szall" class="sz">&mdash;</span>
    </div>
  </div>

  <div class="tabs">
    <button class="tab on" data-tab="fn" data-t="tab.fn">Chức năng</button>
    <button class="tab" data-tab="trim" data-t="tab.trim">Hỗ trợ cắt ghép</button>
    <button class="tab" data-tab="qr" data-t="tab.qr">Xoá QR code</button>
    <button class="tab" data-tab="ver" data-t="tab.ver">Phiên bản</button>
    <button class="tab" data-tab="author" data-t="tab.author">Tác giả</button>
  </div>

  <div id="tab-fn">

  <h2 data-t="h2.step1">1 &middot; Chọn việc muốn làm</h2>
  <div class="card opts">
    <label class="opt"><input type="radio" name="mode" value="games" checked><span>
      <b data-t="opt.games.t">Lược bỏ thời gian chờ turn đối thủ, tách nhiều video cho nhiều đối</b>
      <i data-th="opt.games.d">Mỗi game một video, mỗi cái một timeline riêng, tên
         <code>[ngày] Opponent (game 1).mp4</code>. Tách theo game chứ không
         theo tên đối thủ.</i>
    </span></label>
    <label class="opt"><input type="radio" name="mode" value="full"><span>
      <b data-t="opt.full.t">Lược bỏ thời gian chờ turn đối thủ, gộp 1 video</b>
      <i data-th="opt.full.d">Một video hoàn chỉnh, kèm 1 file timeline .txt để dán vào mô tả
         YouTube. Đây là cái để đăng.</i>
    </span></label>
    <label class="opt"><input type="radio" name="mode" value="download"><span>
      <b data-t="opt.download.t">Chỉ tải video về, không cắt</b>
      <i data-th="opt.download.d">Lưu nguyên bản vào <code class="p-in">input\</code> rồi dừng. Để tải
         sẵn lúc mạng khoẻ, cắt sau — hoặc để giữ lại bản gốc.</i>
    </span></label>
    <details class="dev">
    <summary data-t="dev.summary">Tuỳ chọn cho lập trình viên</summary>
    <label class="opt"><input type="radio" name="mode" value="parts"><span>
      <b data-t="opt.parts.t">Cắt thành nhiều đoạn rời</b>
      <i data-th="opt.parts.d">Mỗi đoạn giữ lại thành một file riêng, không ghép. Để mở từng đoạn
         xem máy cắt có đúng chỗ không.</i>
    </span></label>
    <label class="opt"><input type="radio" name="mode" value="segments"><span>
      <b data-t="opt.segments.t">Chỉ phân tích, không tạo video</b>
      <i data-th="opt.segments.d">Chỉ ra danh sách khoảng sẽ giữ / sẽ bỏ và danh sách chương.
         Nhanh nhất.</i>
    </span></label>
    </details>
    <dl class="paths">
      <dt data-t="paths.video">Video ra</dt><dd><span class="p-out">output\</span><button
        class="small" data-open="output" data-t="btn.open" data-tt="tip.openFolder"
        title="Mở thư mục này trong Explorer">Mở</button></dd>
      <dt data-t="paths.parts">Đoạn rời ra</dt><dd><span class="p-parts">work\…\parts\</span><button
        class="small" data-open="work" data-t="btn.open" data-tt="tip.openWork"
        title="Mở thư mục work trong Explorer">Mở</button></dd>
    </dl>
  </div>

  <h2 data-t="h2.step2">2 &middot; Chọn nguồn</h2>
  <div class="card">
    <div class="row">
      <input type="text" id="url" data-tp="ph.url" placeholder="Dán link YouTube: https://www.youtube.com/watch?v=..." autocomplete="off">
      <button class="small" id="chopen" data-t="btn.chopen" data-tt="tip.chopen"
        title="Mở danh sách stream của kênh để lấy link">Chọn từ kênh&hellip;</button>
      <button class="go" id="start" data-t="btn.start">Tải &amp; chạy</button>
    </div>
    <div class="note" id="startmsg"></div>
    <div class="sep"><span data-t="sep.orRun">hoặc chạy một file đã có trong</span>
      <code class="p-in">input\</code>
      <button class="small" data-open="input" data-t="btn.open"
        data-tt="tip.openInput" title="Mở thư mục input trong Explorer">Mở</button></div>
    <div class="files" id="inputs"><div class="empty" data-t="empty.reading">đang đọc…</div></div>
  </div>


  <h2 data-t="h2.jobs">Công việc</h2>
  <div id="jobs"><div class="card empty" data-t="empty.jobs">Chưa có việc nào. Dán link ở trên để bắt đầu.</div></div>

  </div><!-- /tab-fn -->

  <div id="tab-trim" hidden>
  <h2 data-t="h2.trim">Cắt một đoạn ra file riêng</h2>
  <div class="card">
    <div class="note" data-th="trim.intro"><ul>
      <li>Chọn video trong <code class="p-in">input\</code> hoặc
        <code class="p-out">output\</code>, tua tới chỗ cần rồi bấm
        <b>Đặt tại đây</b>.</li>
      <li>Đoạn cắt ra nằm cùng thư mục với bản gốc, chạy được ngay ở tab
        <b>Chức năng</b> &mdash; để thử thuật toán trên 15 phút thay vì 4
        tiếng.</li></ul></div>
    <div class="row">
      <select id="tsrc"></select>
      <button class="small" id="tload" data-t="btn.preview"
        data-tt="tip.preview" title="Nạp video này vào khung xem">Xem</button>
    </div>
    <video id="tvid" class="prev" controls preload="metadata"></video>
    <div class="marks">
      <label for="tstart" data-t="lbl.start">Điểm đầu</label>
      <input type="text" id="tstart" value="0:00" autocomplete="off">
      <button class="small" data-set="start" data-t="btn.setHere">Đặt tại đây</button>
      <button class="small" data-goto="start" data-t="btn.goto">Tới</button>
      <span class="gap"></span>
      <label for="tend" data-t="lbl.end">Điểm cuối</label>
      <input type="text" id="tend" value="" autocomplete="off">
      <button class="small" data-set="end" data-t="btn.setHere">Đặt tại đây</button>
      <button class="small" data-goto="end" data-t="btn.goto">Tới</button>
    </div>
    <div class="marks act">
      <button class="go" id="tcut" data-t="btn.cut">Cắt đoạn này ra</button>
      <span class="n" id="tinfo"></span>
    </div>
    <div class="note" id="tmsg"></div>
    <div class="note" data-th="trim.note"><ul>
      <li>Copy nguyên luồng, không encode lại: 90 phút xong trong vài giây, và
        hình y hệt bản gốc.</li>
      <li>Đổi lại điểm đầu bám vào keyframe gần nhất phía trước, nên đoạn ra
        có thể dài hơn yêu cầu vài giây &mdash; cắt nhỏ để chạy thử thì không
        ảnh hưởng gì.</li></ul></div>
  </div>
  </div><!-- /tab-trim -->

  <div id="tab-qr" hidden>
  <h2 data-t="h2.qr">Xoá QR code khỏi video</h2>
  <div class="card">
    <div class="note" data-th="qr.intro"><ul>
      <li>Chọn video trong <code class="p-in">input\</code> hoặc
        <code class="p-out">output\</code>, rồi bấm <b>Xoá QR</b>.</li>
      <li>File mới nằm cùng thư mục với bản gốc, tên thêm
        <code>[remove-qr]</code> ở đầu.</li>
      <li>Bản gốc không bị đụng vào.</li></ul></div>
    <div class="row">
      <select id="qsrc"></select>
      <button class="small" id="qload" data-t="btn.preview"
        data-tt="tip.preview" title="Nạp video này vào khung xem">Xem</button>
    </div>
    <video id="qvid" class="prev" controls preload="metadata"></video>
    <div class="marks act">
      <button class="go" id="qgo" data-t="btn.removeQr">Xoá QR</button>
      <span class="n" id="qinfo"></span>
    </div>
    <div class="note" id="qmsg"></div>
    <div class="note" data-th="qr.note"><ul>
      <li>Mã QR đứng yên suốt cả stream, nên nó chỉ được dò một lần rồi phủ
        ảnh lên toàn bộ video.</li>
      <li>Việc này encode lại cả file nên lâu ngang một lần cắt — theo dõi ở
        tab <b>Chức năng</b>, mục <b>Công việc</b>.</li>
      <li>Không dò ra thì vẫn phủ vào đúng góc đó với viền rộng hơn, và báo rõ
        trong log.</li></ul></div>
  </div>
  </div><!-- /tab-qr -->

  <div id="tab-ver" hidden>
  <h2 data-t="h2.ver">Phiên bản</h2>
  <div class="card">
    <dl class="rel">
      <dt class="now"><b>__VERSION__</b> <span class="tag"
        data-t="ver.current">hiện tại</span></dt>
      <dd class="now" data-th="ver.3.0.d"><ul>
        <li>Cắt được video ở mọi độ phân giải 16:9 &mdash; 720p, 1080p, 1440p.
          Video ra giữ nguyên độ phân giải của bản gốc.</li>
        <li>Tải về ở độ phân giải gốc thay vì ép xuống 1080p.</li>
        <li>Giữ nguyên tốc độ khung hình của bản gốc thay vì ép 60 &mdash; file
          nhỏ hơn khoảng 13% và render nhanh hơn, hình y hệt.</li>
        <li>Video không phải 16:9 bị từ chối thẳng, kèm lý do.</li>
        <li>Không còn đổ lỗi đỏ ra cửa sổ đen khi trình duyệt ngắt kết nối.</li>
      </ul></dd>
      <dt><b>2.0</b></dt>
      <dd data-th="ver.2.0.d"><ul>
        <li>Sửa lỗi cắt ngược: đọc nhầm ghế nên giữ lượt đối thủ và cắt lượt
          Tieulinh.</li>
        <li>Không còn sót mẩu lượt đối thủ ở đầu và cuối mỗi lượt.</li>
        <li>Thêm <b>Xoá QR code</b>: dò mã QR một lần rồi phủ logo kênh lên cả
          video.</li>
        <li>Hỗ trợ cắt ghép lấy video từ cả <code class="p-in">input\</code>
          lẫn <code class="p-out">output\</code>.</li>
        <li>Sửa nút <b>Mở thư mục</b> ở mục Công việc: mở sai chỗ và nuốt lỗi
          im lặng.</li>
      </ul></dd>
      <dt><b>1.0</b></dt>
      <dd data-th="ver.1.0.d"><ul>
        <li>Tự cắt bỏ thời gian chờ lượt đối thủ, ghép lại có fade đen.</li>
        <li>Tải VOD từ link YouTube.</li>
        <li>Viết timeline chương theo ngày trong game, dán thẳng vào mô tả.</li>
        <li>Tách riêng từng ván thành video rời.</li>
        <li>Trang web theo dõi tiến độ, và tab hỗ trợ cắt thử một đoạn.</li>
      </ul></dd>
    </dl>
  </div>
  </div><!-- /tab-ver -->

  <div id="tab-author" hidden>
  <h2 data-t="h2.author">Tác giả</h2>
  <div class="card">
    <dl class="kv">
      <dt data-t="author.dev">Dev</dt><dd>Nguyễn Thanh Hải</dd>
      <dt data-t="author.email">Email</dt><dd><a class="mail"
        href="mailto:nguyenthanhhaid13cn7@gmail.com"
        >nguyenthanhhaid13cn7@gmail.com</a>
        <button class="small" data-copy-text="nguyenthanhhaid13cn7@gmail.com"
          data-t="btn.copy" data-tt="tip.copyEmail"
          title="Copy email vào clipboard">Copy</button></dd>
      <dt data-t="author.page">Giới thiệu</dt><dd><a class="mail"
        href="https://darkness0710.github.io/about/"
        target="_blank" rel="noreferrer"
        >darkness0710.github.io/about</a></dd>
    </dl>
  </div>
  </div><!-- /tab-author -->

  <div class="modal" id="chmodal" hidden>
    <div class="sheet">
      <div class="head">
        <b>Stream của kênh</b>
        <select id="chchan"></select>
        <select id="chlimit">
          <option value="10">10 mới nhất</option>
          <option value="20">20 mới nhất</option>
          <option value="100">100 mới nhất</option>
        </select>
        <button class="small" id="chload">Tải lại</button>
        <span class="n" id="chnote"></span>
        <button class="small" id="chclose">Đóng</button>
      </div>
      <div id="chlist"></div>
    </div>
  </div>

  <div class="foot" data-th="foot"><ul>
    <li>Việc chỉ chạy khi cửa sổ đen (server) còn mở — đóng nó là mọi việc
      đang chạy bị dừng theo, kể cả ffmpeg.</li>
    <li>File tải dở vẫn resume được ở lượt sau.</li>
    <li>Trang này không thấy được việc chạy từ Start.cmd.</li>
  </ul></div>
</div>

<script>
const GIB = 1073741824;
function gib(n) { return (n / GIB).toFixed(2) + " GiB"; }
// GiB once it is worth it, MiB below: "0.06 GiB" reads as nothing.
function size(n) {
  if (!n) return "0";
  return n >= GIB ? (n / GIB).toFixed(2) + " GiB"
                  : (n / (1024 * 1024)).toFixed(0) + " MiB";
}
function esc(s) { const d = document.createElement("div"); d.textContent = s == null ? "" : s; return d.innerHTML; }
// How long something took, rounded, with the unit spelled out.
//
// This was called secs() -- the same name as the trim tab's timestamp PARSER
// eight hundred lines further down. Two function declarations with one name in
// one script scope: the later one wins, so every duration on a job card went
// through the parser, which hands back whatever number it is given, and the
// card read "mất 3.4437496662139893". It had done that since 1.0. The names
// are now different jobs with different names.
//
// Units in words, not "3s": the number is read by someone deciding whether to
// wait, and "45 giây" answers that where a bare figure makes them work out
// what it is counting.
function howLong(n) {
  n = Math.max(0, Math.round(n));
  if (n < 60) return n + " giây";
  const m = Math.floor(n / 60), s = n % 60;
  if (m < 60) return s ? m + " phút " + s + " giây" : m + " phút";
  const h = Math.floor(m / 60), mm = m % 60;
  return mm ? h + " giờ " + mm + " phút" : h + " giờ";
}
function pad(n) { return String(n).padStart(2, "0"); }
function stamp(t, timeOnly) {
  if (!t) return "";
  const d = new Date(t * 1000);
  const clock = pad(d.getHours()) + ":" + pad(d.getMinutes()) + ":" + pad(d.getSeconds());
  if (timeOnly) return clock;
  return pad(d.getDate()) + "/" + pad(d.getMonth() + 1) + "/" + d.getFullYear() +
         "  " + clock;
}
// "bắt đầu <khi nào> · xong <khi nào> · <bao lâu>", với ngày chỉ nhắc lại khi
// việc chạy vắt qua nửa đêm.
// Which of our folders this job's result is sitting in.
//
// Three sources, most reliable first. j.where is the job saying so outright.
// Failing that the output PATH, which is the only thing that knows for a
// record written before jobs carried a folder -- and those records are the
// reason this is not just a mode lookup: a QR scrub writes beside its source,
// so it lands in input/ as readily as output/, and guessing "output" because
// a file was produced sent Explorer to the wrong folder. Mode is the last
// resort, for a job that has not produced anything yet.
function jobFolder(j) {
  if (j.where) return j.where;
  const SEP = String.fromCharCode(92);
  const low = String(j.output || "").toLowerCase();
  if (low) {
    for (const w of ["input", "output", "work"])
      if (low.indexOf(SEP + w + SEP) >= 0) return w;
  }
  if (j.mode === "download") return "input";
  if (j.output) return "output";
  return j.mode === "parts" ? "work" : "";
}

function whenLine(j, now) {
  if (!j.started) return "";
  const sameDay = j.finished &&
    new Date(j.started * 1000).toDateString() === new Date(j.finished * 1000).toDateString();
  const parts = ["Bắt đầu <b>" + stamp(j.started) + "</b>"];
  if (j.finished) parts.push("xong <b>" + stamp(j.finished, sameDay) + "</b>");
  parts.push((j.finished ? "mất " : "đã chạy ") +
             "<b>" + howLong((j.finished || now) - j.started) + "</b>");
  return parts.join("   ·   ");
}

const STAGES = {
  queued:      ["Đang xếp hàng", ""],
  downloading: ["Đang tải", "run"],
  analysing:   ["Đang phân tích", "run"],
  rendering:   ["Đang cắt & render", "run"],
  done:        ["Xong", "done"],
  failed:      ["Lỗi", "bad"],
  cancelled:   ["Đã dừng", "bad"],
  interrupted: ["Bị ngắt", "bad"],
};
const ACTIVE = ["queued", "downloading", "analysing", "rendering"];
// ------------------------------------------------------------------ i18n ---
// Both languages arrive with the page: 124 short strings, which is smaller
// than one thumbnail and saves a request and a loading state.
const STRINGS = /*__I18N__*/{};
const FALLBACK = /*__LANG__*/"vi";

function readLang() {
  let want = null;
  try { want = localStorage.getItem("lang"); } catch (e) { want = null; }
  return STRINGS[want] ? want : FALLBACK;
}
let LANG = readLang();

// A key with no translation falls back to the default language rather than
// showing blank: a missing string should look wrong, not look empty.
function T(key) {
  const table = STRINGS[LANG] || {};
  if (key in table) return table[key];
  const base = STRINGS[FALLBACK] || {};
  return key in base ? base[key] : key;
}

// data-t sets text, data-th sets markup (for the few strings carrying <code>
// or <b>), data-tt a tooltip, data-tp a placeholder.
function applyLang() {
  document.documentElement.lang = LANG;
  for (const el of document.querySelectorAll("[data-t]"))
    el.textContent = T(el.dataset.t);
  for (const el of document.querySelectorAll("[data-th]"))
    el.innerHTML = T(el.dataset.th);
  for (const el of document.querySelectorAll("[data-tt]"))
    el.title = T(el.dataset.tt);
  for (const el of document.querySelectorAll("[data-tp]"))
    el.placeholder = T(el.dataset.tp);
  for (const b of document.querySelectorAll(".langs button"))
    b.classList.toggle("on", b.dataset.lang === LANG);
  document.getElementById("start").textContent =
    mode() === "download" ? T("btn.startDl") : T("btn.start");
  // data-th rebuilt the <code class="p-in"> spans, so the paths in them are
  // back to their placeholder text until the next poll. Ask for one now.
  if (LAST) refresh();
}

for (const b of document.querySelectorAll(".langs button")) {
  b.onclick = () => {
    LANG = b.dataset.lang;
    try { localStorage.setItem("lang", LANG); } catch (e) { /* private mode */ }
    applyLang();
  };
}

const MODES = { full: "gộp 1 video", games: "tách theo game",
                download: "chỉ tải về", parts: "nhiều đoạn rời",
                segments: "chỉ phân tích" };

// The mode is chosen once, at the top, and both sources use it.
function mode() {
  const el = document.querySelector('input[name=mode]:checked');
  return el ? el.value : "full";
}

// The mode changes what both buttons mean. Say so on the click rather than
// on the next poll a second later.
for (const el of document.querySelectorAll("input[name=mode]")) {
  el.addEventListener("change", () => {
    document.getElementById("start").textContent =
      mode() === "download" ? "Tải về" : "Tải & chạy";
    refresh();
  });
}

// ------------------------------------------------------------------ tabs ---
for (const b of document.querySelectorAll(".tabs button")) {
  b.onclick = () => {
    for (const other of document.querySelectorAll(".tabs button"))
      other.classList.toggle("on", other === b);
    for (const other of document.querySelectorAll(".tabs button"))
      document.getElementById("tab-" + other.dataset.tab).hidden =
        other !== b;
    if (b.dataset.tab === "trim") trimSources(LAST);
    if (b.dataset.tab === "qr") qrSources(LAST);
  };
}

let openLogs = new Set();
let LAST = null;                 // the last state, so a copy can carry context

// localhost counts as a secure context, so the clipboard API is available;
// the textarea is there for a browser that still refuses.
function hms(n) {
  if (!n) return "";
  n = Math.round(n);
  const h = Math.floor(n / 3600), m = Math.floor((n % 3600) / 60);
  return h ? h + ":" + pad(m) + ":" + pad(n % 60) : m + ":" + pad(n % 60);
}
function thousands(n) {
  return n == null ? "" : String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}

async function copyText(text) {
  try { await navigator.clipboard.writeText(text); return true; } catch (e) {}
  try {
    const ta = document.createElement("textarea");
    ta.value = text;
    document.body.appendChild(ta);
    ta.select();
    const ok = document.execCommand("copy");
    document.body.removeChild(ta);
    return ok;
  } catch (e) { return false; }
}

// What a job looks like as pasteable text: the record first, then the log,
// so one paste says what was run as well as what it printed.
const COPY_FIELDS = [["title", "Tên"], ["mode", "Chế độ"], ["stage", "Bước"],
  ["percent", "%"], ["detail", "Chi tiết"], ["url", "URL"], ["file", "File"],
  ["size", "Dung lượng tải"], ["streams", "Luồng"], ["downloader", "Downloader"],
  ["length", "Thời lượng"], ["segments", "Segment"], ["kept", "Giữ"],
  ["chapters", "Chương"], ["output", "Video ra"], ["output_size", "Cỡ output"],
  ["chapters_path", "Timeline (.txt)"],
  ["warning", "Cảnh báo"], ["error", "Lỗi"]];

function jobAsText(job, log) {
  const NL = String.fromCharCode(10);
  const out = ["tieu_linh_hota job " + job.id];
  if (job.started) out.push("Bắt đầu: " + stamp(job.started));
  if (job.finished) out.push("Kết thúc: " + stamp(job.finished),
                             "Mất: " + howLong(job.finished - job.started));
  for (const [key, label] of COPY_FIELDS)
    if (job[key] !== undefined && job[key] !== null && job[key] !== "")
      out.push(label + ": " + job[key]);
  out.push("", "---- log (" + (log || []).length + " dòng) ----", "");
  return out.concat(log || []).join(NL);
}

// Two buttons, nothing to type. Every destructive action goes through here.
function ask(...lines) {
  return confirm(lines.join(String.fromCharCode(10)));
}

async function post(path, body) {
  const r = await fetch(path, { method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body || {}) });
  return { ok: r.ok, data: await r.json().catch(() => ({})) };
}

function note(text, bad) {
  const el = document.getElementById("startmsg");
  el.className = bad ? "note bad" : "note";
  el.textContent = text;
}

// Every Explorer button goes through here. They used to be `void post(...)`,
// which discards the reply: when the server answered "không còn file đó" the
// click simply did nothing at all, with no way to tell a failure from a
// window that opened behind the browser. Opening a folder is not important
// enough to interrupt, but it is important enough to admit when it did not.
async function reveal(where, file) {
  const { ok, data } = await post("/api/reveal", { where: where, file: file });
  // This endpoint reports a refusal as {opened:false, message}, not {error},
  // so read both: the server's own wording ("không còn file đó") says more
  // than any generic line here can.
  if (!ok || data.opened === false)
    note(data.error || data.message || T("reveal.failed"), true);
}

async function startJob(payload) {
  const btn = document.getElementById("start");
  btn.disabled = true;
  const msg = document.getElementById("startmsg");
  msg.className = "note"; msg.textContent = "";
  const { ok, data } = await post("/api/jobs", payload);
  btn.disabled = false;
  if (!ok) { msg.className = "note bad"; msg.textContent = data.error || "không bắt đầu được"; }
  else { document.getElementById("url").value = ""; refresh(); }
}

document.getElementById("start").onclick = () => startJob({
  url: document.getElementById("url").value, mode: mode() });
document.getElementById("url").addEventListener("keydown", e => {
  if (e.key === "Enter") document.getElementById("start").click(); });

function jobCard(j, now) {
  const [label, cls] = STAGES[j.stage] || [j.stage, ""];
  const active = ACTIVE.includes(j.stage);
  const idle = now - (j.updated || 0);
  let html = '<div class="card job">';
  html += '<div class="head"><span class="t">' + esc(j.title || j.file || j.url) + '</span>';
  html += '<span class="badge ' + cls + '">' + label + (active ? " " + (j.percent || 0) + "%" : "") + '</span>';
  if (active) html += '<button class="small" data-cancel="' + j.id + '">Dừng</button>';
  else html += '<button class="small danger" data-jobdel="' + j.id + '" ' +
               'title="Xoá việc này khỏi danh sách. Không xoá video.">Xoá</button>';
  html += '<button class="small" data-log="' + j.id + '">Chi tiết</button>';
  html += '<button class="small" data-copy="' + j.id + '" ' +
          'title="Copy toàn bộ log + thông tin việc này vào clipboard">Copy log</button>';
  // Where the result of this job landed: output\ for a finished video,
  // work\ for the loose pieces.
  const home = jobFolder(j);
  if (home && !active)
    html += '<button class="small" data-openjob="' + j.id + '" ' +
            'data-where="' + home + '" title="Mở thư mục chứa kết quả">Mở thư mục</button>';
  html += '</div>';
  const when = whenLine(j, now);
  if (when) html += '<div class="when">' + when + '</div>';
  if (active) html += '<div class="prog"><i style="width:' + (j.percent || 0) + '%"></i></div>';
  if (j.detail) html += '<div class="meta">' + esc(j.detail) + '</div>';

  // A bar that stops moving and an app that has hung look identical, so say
  // how long it has been quiet rather than leaving it to be guessed -- but
  // scale the threshold by how often this job reports, or a render that
  // prints once per piece is called stuck between every two pieces.
  const quiet = Math.max(20, (j.gap || 0) * 2.5);
  if (active && idle > quiet)
    html += '<div class="note warn">Không có dữ liệu mới trong ' + howLong(idle) + '.</div>';
  if (j.warning) html += '<div class="note warn">' + esc(j.warning) + '</div>';
  if (j.error) html += '<div class="note bad">' + esc(j.error) + '</div>';

  const kv = [];
  if (j.mode && j.mode !== "full") kv.push(["Chế độ", MODES[j.mode] || j.mode]);
  if (j.size) kv.push(["Dung lượng tải", j.size]);
  if (j.streams) kv.push(["Luồng", j.streams]);
  if (j.downloader) kv.push(["Downloader", j.downloader]);
  if (j.length) kv.push(["Thời lượng", j.length]);
  if (j.segments != null) kv.push(["Segment", j.segments + (j.kept ? " · giữ " + j.kept : "")]);
  if (j.chapters != null) kv.push(["Chương", String(j.chapters)]);
  if (j.file) kv.push(["File nguồn", j.file]);
  if (j.output) kv.push([j.mode === "download" ? "File đã tải" : "Video ra",
                         j.output + (j.output_size ? "  (" + j.output_size + ")" : "")]);
  if (j.chapters_path) kv.push(["Timeline (.txt)", j.chapters_path]);

  if (kv.length) {
    html += '<dl class="kv">';
    for (const [k, v] of kv) html += "<dt>" + esc(k) + "</dt><dd>" + esc(v) + "</dd>";
    html += "</dl>";
  }
  if (openLogs.has(j.id)) html += '<pre id="log-' + j.id + '">đang tải log…</pre>';
  html += "</div>";
  return html;
}

async function loadLog(id) {
  const el = document.getElementById("log-" + id);
  if (!el) return;
  const r = await fetch("/api/jobs/" + id + "/log");
  const d = await r.json().catch(() => ({ log: [] }));
  el.textContent = (d.log || []).slice(-200).join("\n") || "(chưa có gì)";
  el.scrollTop = el.scrollHeight;
}

async function refresh() {
  let s;
  try { s = await (await fetch("/api/state")).json(); }
  catch (e) { return; }
  LAST = s;

  // The folders are only known at run time, and a person looking for a file
  // in Explorer needs the whole path, not "output\".
  const P = s.paths || {};
  const put = (sel, value) => document.querySelectorAll(sel)
    .forEach(el => { if (value) el.textContent = value; });
  put(".p-out", P.output ? P.output + "\\" : "");
  put(".p-in", P.input ? P.input + "\\" : "");
  put(".p-work", P.work ? P.work + "\\" : "");
  put(".p-parts", P.parts || "");

  const F = s.folders || {};
  for (const [id, key] of [["szin", "input"], ["szout", "output"],
                           ["szwork", "work"]]) {
    const f = F[key] || {};
    document.getElementById(id).textContent =
      size(f.bytes) + "   " + (f.files || 0) + " file";
  }
  // The total on the Dọn tất cả button comes from the server's `clear` block,
  // not from adding up the three folder sizes: work/ keeps index.json, so the
  // two numbers are not the same and the button must promise the smaller one.
  const A = ((s.clear || {}).all) || {};
  document.getElementById("szall").textContent =
    A.files ? size(A.bytes) + "   " + A.files + " file" : "không có gì";

  const d = s.drive, pct = d.total ? Math.round(100 * d.used / d.total) : 0;
  document.getElementById("dv").textContent = "Ổ " + d.root;
  document.getElementById("dvbar").style.width = pct + "%";
  document.getElementById("dvfree").textContent =
    "còn " + gib(d.free) + " / " + gib(d.total);

  const inputs = document.getElementById("inputs");
  if (!s.inputs.length) {
    inputs.innerHTML = '<div class="empty">Chưa có video nào ở đây.</div>';
  } else {
    const noRun = mode() === "download";
    inputs.innerHTML = s.inputs.map(f =>
      '<div class="file"><span class="nm">' + esc(f.name) + '</span>' +
      '<span class="sz">' + size(f.bytes) + "</span>" +
      '<button class="small" data-run="' + esc(f.name) + '"' +
        (noRun ? ' disabled title="Đang chọn chế độ chỉ tải về, ' +
                 'file này thì đã tải rồi"' : '') + '>Chạy</button>' +
      '<button class="small" data-show="' + esc(f.name) + '" ' +
        'title="Mở thư mục chứa file này, chọn sẵn nó">Mở</button>' +
      '<button class="small danger" data-del="' + esc(f.name) + '" data-size="' +
        gib(f.bytes) + '" title="Chuyển vào Thùng rác, có thể phục hồi">Xoá</button>' +
      "</div>").join("");
  }

  if (!document.getElementById("tab-trim").hidden) trimSources(s);
  if (!document.getElementById("tab-qr").hidden) qrSources(s);

  const jobs = document.getElementById("jobs");
  jobs.innerHTML = s.jobs.length
    ? s.jobs.map(j => jobCard(j, s.now)).join("")
    : '<div class="card empty">Chưa có việc nào. Dán link ở trên để bắt đầu.</div>';
  for (const id of openLogs) loadLog(id);
}

document.addEventListener("click", async e => {
  const run = e.target.closest("[data-run]");
  if (run) return startJob({ file: run.dataset.run, mode: mode() });
  const oj = e.target.closest("[data-openjob]");
  if (oj) {
    const job = ((LAST && LAST.jobs) || []).find(j => j.id === oj.dataset.openjob) || {};
    const SEP = String.fromCharCode(92);
    const leaf = job.output ? job.output.split(SEP).pop() : null;
    return void reveal(oj.dataset.where, leaf);
  }
  const go = e.target.closest("[data-gotab]");
  if (go) {
    const tab = document.querySelector('.tabs button[data-tab="'
                                       + go.dataset.gotab + '"]');
    if (tab) { tab.click(); tab.scrollIntoView({block: "nearest"}); }
    return;
  }
  const open = e.target.closest("[data-open]");
  if (open) return void reveal(open.dataset.open);
  const show = e.target.closest("[data-show]");
  if (show) return void reveal("input", show.dataset.show);
  const ct = e.target.closest("[data-copy-text]");
  if (ct) {
    const was = ct.textContent;
    ct.textContent = (await copyText(ct.dataset.copyText)) ? "Đã copy"
                                                           : "Không copy được";
    setTimeout(() => { ct.textContent = was; }, 1500);
    return;
  }
  const cp = e.target.closest("[data-copy]");
  if (cp) {
    const id = cp.dataset.copy;
    const was = cp.textContent;
    cp.textContent = "...";
    let log = [];
    try {
      const r = await fetch("/api/jobs/" + id + "/log");
      log = (await r.json()).log || [];
    } catch (e) {}
    const job = ((LAST && LAST.jobs) || []).find(j => j.id === id) || { id: id };
    const ok = await copyText(jobAsText(job, log));
    cp.textContent = ok ? "Đã copy" : "Không copy được";
    setTimeout(() => { cp.textContent = was; }, 1800);
    return;
  }
  const clr = e.target.closest("[data-clear]");
  if (clr) {
    const key = clr.dataset.clear;
    // Size from `clear`, not `folders`: this is what the server will actually
    // recycle, so the figure in the dialog is the figure that goes.
    const C = ((LAST && LAST.clear) || {})[key] || {};
    const P = (LAST && LAST.paths) || {};
    if (!C.files) { note("Không có gì để dọn."); return; }
    const lines = key === "all"
      ? ["Dọn TẤT CẢ?", "",
         P.input + "\\", P.output + "\\", P.work + "\\   (kèm cache phân tích)", "",
         C.files + " file, " + size(C.bytes), "",
         "Gồm cả video gốc đã tải và video đã cắt.",
         "Cache phân tích mất theo, nên lần cắt sau phải phân tích lại.",
         "Tất cả sẽ được chuyển vào Thùng rác, có thể phục hồi."]
      : key === "work"
      ? ["Dọn thư mục tạm?", "", P.work + "\\", "",
         C.files + " file, " + size(C.bytes), "",
         "Gồm cache phân tích, nên lần cắt sau phải phân tích lại,",
         "và gồm cả lịch sử việc đã chạy hiện trên trang này.",
         "Video trong input\\ và output\\ KHÔNG bị xoá.",
         "Tất cả sẽ được chuyển vào Thùng rác, có thể phục hồi."]
      : ["Dọn sạch thư mục này?", "", (P[key] || key) + "\\", "",
         C.files + " file, " + size(C.bytes), "",
         "Tất cả sẽ được chuyển vào Thùng rác, có thể phục hồi."];
    if (!ask.apply(null, lines)) return;
    const { ok, data } = await post("/api/folders/clear", { where: key });
    note(ok ? (data.message || "đã dọn") : (data.error || "không dọn được"), !ok);
    return refresh();
  }
  const del = e.target.closest("[data-del]");
  if (del) {
    const name = del.dataset.del;
    if (!ask("Xoá file này?", "", name, "(" + del.dataset.size + ")", "",
             "File sẽ được chuyển vào Thùng rác, có thể phục hồi.")) return;
    const { ok, data } = await post("/api/files/delete", { file: name });
    note(ok ? "Đã chuyển vào Thùng rác: " + name
            : (data.error || "không xoá được"), !ok);
    return refresh();
  }
  const jd = e.target.closest("[data-jobdel]");
  if (jd) {
    const id = jd.dataset.jobdel;
    const job = ((LAST && LAST.jobs) || []).find(j => j.id === id) || {};
    if (!ask("Xoá việc này khỏi danh sách?", "", job.title || id, "",
             "Chỉ xoá bản ghi và log của việc.",
             "Video đã tải và video đã cắt KHÔNG bị xoá.")) return;
    const { ok, data } = await post("/api/jobs/" + id + "/delete", {});
    const msg = document.getElementById("startmsg");
    msg.className = ok ? "note" : "note bad";
    msg.textContent = ok ? "Đã xoá việc khỏi danh sách."
                         : (data.error || "không xoá được");
    return refresh();
  }
  const cancel = e.target.closest("[data-cancel]");
  if (cancel) { await post("/api/jobs/" + cancel.dataset.cancel + "/cancel"); return refresh(); }
  const log = e.target.closest("[data-log]");
  if (log) {
    const id = log.dataset.log;
    openLogs.has(id) ? openLogs.delete(id) : openLogs.add(id);
    return refresh();
  }
});

// ------------------------------------------------------------------ trim ---
// A preview and two marks. The point is not to type a timestamp -- the command
// line is better at that -- but to see the frame and take the time off it.
const tvid = document.getElementById("tvid");

// PARSES a typed timestamp into seconds -- the opposite direction from
// howLong() above, which formats one. "1:02:03", "2:03", "90" and "1h02m03"
// all mean what they look like.
function secs(text) {
  const t = String(text == null ? "" : text).trim()
              .replace(/[hm]/g, ":").replace(/:+$/, "");
  if (!t) return NaN;
  const parts = t.split(":");
  let v = 0;
  for (const part of parts) {
    const n = Number(part);
    if (part === "" || !isFinite(n) || n < 0) return NaN;
    v = v * 60 + n;
  }
  return v;
}

function clock(v) {
  v = Math.max(0, Math.round(v || 0));
  return Math.floor(v / 3600) + ":" + pad(Math.floor((v % 3600) / 60))
         + ":" + pad(v % 60);
}

function tnote(text, bad) {
  const el = document.getElementById("tmsg");
  el.className = bad ? "note bad" : "note";
  el.textContent = text;
}

// Every video in either folder, named "<folder>/<file>".
//
// The folder is part of the VALUE, not decoration on the label: the same
// basename can exist in both -- output/ is full of files cut from input/, and
// a trimmed sample of a cut lands beside the cut -- so a bare name is
// ambiguous the moment both folders are offered. The server resolves the same
// two tokens back, and takes a bare name as input/ so nothing older breaks.
function folderRefs(s) {
  const out = [];
  for (const pair of [["input", (s && s.inputs) || []],
                      ["output", (s && s.outputs) || []]])
    for (const f of pair[1]) out.push(pair[0] + "/" + f.name);
  return out;
}

// Rebuilt only when the file list actually changes, so the poll every second
// does not throw away what the reader picked.
function fillSources(sel, refs, empty) {
  const sig = refs.join("|");
  if (sel.dataset.sig === sig) return;
  sel.dataset.sig = sig;
  const had = sel.value;
  sel.innerHTML = refs.length
    ? refs.map(r => '<option value="' + esc(r) + '">' + esc(r) + "</option>").join("")
    : '<option value="">' + esc(empty) + "</option>";
  if (refs.indexOf(had) >= 0) sel.value = had;
}

function trimSources(s) {
  fillSources(document.getElementById("tsrc"), folderRefs(s), T("trim.noVideo"));
}

function qrSources(s) {
  fillSources(document.getElementById("qsrc"), folderRefs(s), T("trim.noVideo"));
}

function tload() {
  const name = document.getElementById("tsrc").value;
  if (!name) return tnote("Chưa có video nào để xem.", true);
  tvid.src = "/media?name=" + encodeURIComponent(name);
  tvid.load();
  tnote("");
}

document.getElementById("tload").onclick = tload;
document.getElementById("tsrc").onchange = tload;

tvid.addEventListener("loadedmetadata", () => {
  document.getElementById("tend").value = clock(tvid.duration);
  document.getElementById("tstart").value = "0:00:00";
  tinfo();
});
tvid.addEventListener("error", () => tnote(
  "Trình duyệt không phát được file này. mp4 và webm thì được; mkv, ts, avi "
  + "thì thường không, nhưng vẫn cắt được nếu tự nhập mốc.", true));

function tinfo() {
  const a = secs(document.getElementById("tstart").value);
  const b = secs(document.getElementById("tend").value);
  const el = document.getElementById("tinfo");
  if (!isFinite(a) || !isFinite(b)) { el.textContent = "mốc không đọc được"; return; }
  el.textContent = b > a
    ? "dài " + clock(b - a) + "   (" + clock(a) + " → " + clock(b) + ")"
    : "điểm cuối phải sau điểm đầu";
}
for (const id of ["tstart", "tend"])
  document.getElementById(id).addEventListener("input", tinfo);

document.addEventListener("click", e => {
  const set = e.target.closest("[data-set]");
  if (set) {
    document.getElementById("t" + set.dataset.set).value = clock(tvid.currentTime);
    return tinfo();
  }
  const go = e.target.closest("[data-goto]");
  if (go) {
    const v = secs(document.getElementById("t" + go.dataset.goto).value);
    if (isFinite(v)) tvid.currentTime = v;
  }
});

document.getElementById("tcut").onclick = async () => {
  const name = document.getElementById("tsrc").value;
  const a = secs(document.getElementById("tstart").value);
  const b = secs(document.getElementById("tend").value);
  if (!name) return tnote("Chưa chọn video.", true);
  if (!isFinite(a) || !isFinite(b) || b <= a)
    return tnote("Mốc thời gian không hợp lệ.", true);
  if (!ask("Cắt đoạn này ra thành file mới?", "", name, "",
           clock(a) + " → " + clock(b) + "   (dài " + clock(b - a) + ")", "",
           T("trim.sameFolder")))
    return;
  const btn = document.getElementById("tcut");
  btn.disabled = true;
  tnote("đang cắt…");
  const { ok, data } = await post("/api/trim", { name: name, start: a, end: b });
  btn.disabled = false;
  if (!ok) return tnote(data.error || "không cắt được", true);
  tnote("Đã cắt: " + data.name + "   " + size(data.bytes)
        + "   dài thật " + clock(data.length)
        + (data.length - (b - a) > 1.5 ? "  (dài hơn yêu cầu do bám keyframe)" : ""));
  refresh();
};

// --------------------------------------------------------------- remove QR ---
// Its own preview and one button. Deliberately no marks: this is the whole
// file or nothing, because the QR is on screen for the whole file.
const qvid = document.getElementById("qvid");

function qnote(text, bad) {
  const el = document.getElementById("qmsg");
  el.className = bad ? "note bad" : "note";
  el.textContent = text;
}

function qload() {
  const ref = document.getElementById("qsrc").value;
  if (!ref) return qnote(T("trim.pickFirst"), true);
  qvid.src = "/media?name=" + encodeURIComponent(ref);
  qvid.load();
  qnote("");
}

document.getElementById("qload").onclick = qload;
document.getElementById("qsrc").onchange = () => {
  document.getElementById("qinfo").textContent = "";
  qload();
};
qvid.addEventListener("loadedmetadata", () => {
  document.getElementById("qinfo").textContent = "dài " + clock(qvid.duration);
});
qvid.addEventListener("error", () => qnote(T("trim.cantPlay"), true));

document.getElementById("qgo").onclick = async () => {
  const ref = document.getElementById("qsrc").value;
  if (!ref) return qnote(T("trim.noSource"), true);
  const slash = ref.indexOf("/");
  const where = ref.slice(0, slash), name = ref.slice(slash + 1);
  if (!ask(T("qr.askTitle"), "", ref, "",
           T("qr.askOut") + "  " + where + "\[remove-qr] " + name, "",
           T("qr.askNote")))
    return;
  const btn = document.getElementById("qgo");
  btn.disabled = true;
  qnote(T("qr.starting"));
  const { ok, data } = await post("/api/remove-qr", { name: ref });
  btn.disabled = false;
  if (!ok) return qnote(data.error || T("qr.failed"), true);
  qnote(data.message || T("qr.started"));
  refresh();
};

// ---------------------------------------------------------------- channel ---
// A picker, deliberately separate from the rest of the page: it hands back a
// link and changes nothing else. The listing is flat -- no player request per
// video -- which is why a hundred rows take about a second, and also why it
// carries no date. A date is one request per video, so it is fetched only for
// a row somebody asks about.
const chModal = document.getElementById("chmodal");
const chList = document.getElementById("chlist");
const chNote = document.getElementById("chnote");
const chChan = document.getElementById("chchan");

function chShow(open) { chModal.hidden = !open; }

// The channel list comes from the server so there is one list, not two.
// Filled on the first open, then left alone: it does not change while the
// page is up, and refilling it would throw away the reader's choice.
async function chChannels() {
  if (chChan.options.length) return;
  const { ok, data } = await post("/api/channels", {});
  const rows = (ok && data.channels) || [];
  chChan.innerHTML = rows.map(c =>
    '<option value="' + esc(c.url) + '">' + esc(c.name) + "</option>").join("");
}

document.getElementById("chopen").onclick = async () => {
  chShow(true);
  await chChannels();
  chLoad();
};
document.getElementById("chclose").onclick = () => chShow(false);
document.getElementById("chload").onclick = () => chLoad();
document.getElementById("chlimit").onchange = () => chLoad();
chChan.onchange = () => chLoad();
chModal.addEventListener("click", e => { if (e.target === chModal) chShow(false); });
document.addEventListener("keydown", e => {
  if (e.key === "Escape" && !chModal.hidden) chShow(false);
});

async function chLoad() {
  const limit = document.getElementById("chlimit").value;
  chNote.textContent = "đang lấy danh sách…";
  chList.innerHTML = "";
  const { ok, data } = await post("/api/channel",
                                  { limit: Number(limit), url: chChan.value });
  if (!ok) { chNote.textContent = data.error || "không lấy được"; return; }
  const rows = data.entries || [];
  chNote.textContent = rows.length + " video";
  chList.innerHTML = rows.map(v => {
    const live = v.live === "is_live" || v.live === "is_upcoming";
    const meta = [live ? "ĐANG PHÁT" : hms(v.duration),
                  v.views != null ? thousands(v.views) + " view" : ""]
                 .filter(Boolean).join("   \u00b7   ");
    return '<div class="vid' + (live ? " live" : "") + '">' +
      '<img loading="lazy" src="' + esc(v.thumb) + '" alt="">' +
      '<div class="body"><div class="t">' + esc(v.title) + "</div>" +
      '<div class="m">' + esc(meta) + '<span id="d-' + esc(v.id) + '"></span></div>' +
      '<div class="acts">' +
      (live ? '<span class="m">chưa kết thúc, không tải được</span>'
            : '<button class="small" data-use="' + esc(v.url) + '">Dùng link này</button>' +
              '<button class="small" data-cl="' + esc(v.url) + '">Copy link</button>' +
              '<button class="small" data-vd="' + esc(v.id) + '">Ngày phát</button>') +
      "</div></div></div>";
  }).join("") || '<div class="vid"><span class="m">Kênh này chưa có stream nào.</span></div>';
}

document.addEventListener("click", async e => {
  const use = e.target.closest("[data-use]");
  if (use) {
    document.getElementById("url").value = use.dataset.use;
    chShow(false);
    document.getElementById("url").focus();
    return;
  }
  const cl = e.target.closest("[data-cl]");
  if (cl) {
    const was = cl.textContent;
    cl.textContent = (await copyText(cl.dataset.cl)) ? "Đã copy" : "Không copy được";
    setTimeout(() => { cl.textContent = was; }, 1500);
    return;
  }
  const vd = e.target.closest("[data-vd]");
  if (vd) {
    const id = vd.dataset.vd;
    vd.textContent = "...";
    const { ok, data } = await post("/api/video-date", { id: id });
    const slot = document.getElementById("d-" + id);
    if (ok && data.when) {
      if (slot) slot.textContent = "   \u00b7   phát " + stamp(data.when);
      vd.remove();
    } else {
      vd.textContent = "không lấy được";
    }
  }
});

applyLang();
refresh();
setInterval(refresh, 1000);
</script>
</body>
</html>
"""

# One build step, not a format(): the page is full of CSS braces and JS
# template syntax, and a replace of two markers cannot misread any of it.
# The markers carry a dummy value after them, so the template is valid
# JavaScript on its own and node --check can read it before the build; the
# replacement swallows the dummy along with the marker.
PAGE = (_HTML
        .replace("/*__I18N__*/{}",
                 json.dumps(i18n.STRINGS, ensure_ascii=False))
        .replace('/*__LANG__*/"vi"', json.dumps(i18n.DEFAULT))
        .replace("__VERSION__", C.VERSION))
assert "__I18N__" not in PAGE and "__LANG__" not in PAGE
# Both places that show the version come from C.VERSION, and this is what says
# so: a literal left behind in either one would be a number that stops being
# true at the next release, silently.
assert "__VERSION__" not in PAGE
assert PAGE.count(">v" + C.VERSION + "<") == 1, "header badge"
assert PAGE.count("<b>" + C.VERSION + "</b>") == 1, "Version tab row"


def _check_markup():
    """A string carrying markup must be bound with data-th, never data-t.

    applyLang() assigns data-t through textContent and data-th through
    innerHTML, so a string with <b> or <code> in it bound the first way is
    shown to the reader as literal angle brackets. Nothing else catches that:
    it is valid HTML, valid Python and valid JavaScript, and the page renders
    -- wrongly -- rather than failing. It shipped exactly once, on qr.note.

    Checked against BOTH languages: a key can be plain in one and carry markup
    in the other, and the mistake would then only appear after a language
    switch.
    """
    wrong = []
    for key in set().union(*(set(d) for d in i18n.STRINGS.values())):
        if f'data-t="{key}"' not in _HTML:
            continue
        for lang, table in i18n.STRINGS.items():
            if re.search(r"<[a-zA-Z/]", table.get(key, "")):
                wrong.append(f"{key} ({lang})")
    if wrong:
        raise ValueError(
            "these strings carry markup but are bound with data-t, which "
            f"shows the tags as text -- use data-th: {sorted(wrong)}")


_check_markup()
