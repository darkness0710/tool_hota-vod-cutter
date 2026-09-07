<#
    Free up disk space, with a look before the leap.

    This deletes video files -- hours of downloading and rendering -- so it
    shows what it is about to remove and how big it is, asks which group, and
    then asks again. Everything goes to the Recycle Bin, not straight out, so a
    misclick is recoverable.

    Do not run this directly by double-clicking -- Windows opens .ps1 files in
    Notepad. Double-click Clear.cmd in the folder above, which calls this.
#>
[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
# This script lives in scripts\, so the project root is one level up.
$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
Set-Location $root

Add-Type -AssemblyName Microsoft.VisualBasic

function Line { Write-Host ("-" * 66) -ForegroundColor DarkGray }
function GB($bytes) { "{0,7:N2} GiB" -f ($bytes / 1GB) }

function Measure-Set($paths) {
    $files = @($paths | Where-Object { $_ } | ForEach-Object { $_ })
    $bytes = 0
    foreach ($f in $files) { $bytes += $f.Length }
    [pscustomobject]@{ Files = $files; Count = $files.Count; Bytes = $bytes }
}

function Get-Parts {
    if (-not (Test-Path "input")) { return @() }
    Get-ChildItem "input" -File -Filter "*.part" -ErrorAction SilentlyContinue
}
function Get-InputVideos {
    if (-not (Test-Path "input")) { return @() }
    Get-ChildItem "input" -File -ErrorAction SilentlyContinue |
        Where-Object { $_.Extension -ne ".part" }
}
function Get-Output {
    if (-not (Test-Path "output")) { return @() }
    Get-ChildItem "output" -File -Recurse -ErrorAction SilentlyContinue
}
function Get-PartsDirs {
    if (-not (Test-Path "work")) { return @() }
    Get-ChildItem "work" -Directory -Recurse -ErrorAction SilentlyContinue |
        Where-Object { $_.Name -like "parts*" }
}
function Get-LeftoverParts {
    # Rendered segment pieces. A render that finishes deletes its own parts
    # directory, so anything still sitting here was left by a render that
    # failed or was interrupted -- or put there on purpose by debug.cmd /
    # --parts-only, which is why this asks rather than tidying up by itself.
    #
    # These get their own choice because of what they are NOT mixed with.
    # They are the only big thing under work\ -- gigabytes -- while the
    # expensive thing under work\ is signal.npz, a megabyte that costs half an
    # hour of decoding to rebuild. One "work" group meant reclaiming the
    # gigabytes always threw away the cache too, so the honest options are
    # "the big worthless files" and "all of it".
    # -LiteralPath, not a bare path: every downloaded folder name carries the
    # [DD-MM-YYYY] and [videoid] brackets, and PowerShell reads those as a
    # character class. Without it this silently measured 0 files while 1.05 GiB
    # sat in work\ -- the same trap the README flags for --only globs.
    @(Get-PartsDirs) | ForEach-Object {
        Get-ChildItem -LiteralPath $_.FullName -File -Recurse -ErrorAction SilentlyContinue
    }
}
function Get-Work {
    # index.json is deliberately spared. It maps each input to the output it
    # produced, which is what makes re-running skip instead of rendering a
    # duplicate under a "(2)" name. Downloads also carry their date in the
    # filename, so losing the index costs less than it used to, but there is
    # no reason to throw it away with the scratch.
    if (-not (Test-Path "work")) { return @() }
    Get-ChildItem "work" -File -Recurse -ErrorAction SilentlyContinue |
        Where-Object { $_.Name -ne "index.json" }
}

Write-Host ""
Write-Host "  Tieulinh HOTA - clean up" -ForegroundColor Cyan
Write-Host "  Author: Nguyễn Thanh Hải" -ForegroundColor DarkGray
Line

$parts  = Measure-Set (Get-Parts)
$inputs = Measure-Set (Get-InputVideos)
$output = Measure-Set (Get-Output)
$pieces = Measure-Set (Get-LeftoverParts)
$work   = Measure-Set (Get-Work)

function Show-Drive {
    $root = [System.IO.Path]::GetPathRoot((Get-Location).Path)
    $d = Get-PSDrive -PSProvider FileSystem |
         Where-Object { $_.Root -eq $root } | Select-Object -First 1
    if (-not $d) { return }
    $total = $d.Used + $d.Free
    if ($total -le 0) { return }
    $pct = [int](100 * $d.Free / $total)
    $bar = "#" * [int]((100 - $pct) / 4) + "-" * [int]($pct / 4)
    Write-Host ""
    Write-Host ("  Drive {0}  [{1}]" -f $root, $bar)
    Write-Host ("    used {0}   free {1}   of {2}   ({3}% free)" -f `
        (GB $d.Used), (GB $d.Free), (GB $total), $pct) -ForegroundColor DarkGray
}

Show-Drive

Write-Host ""
Write-Host "  What this project is holding:"
Write-Host ""
Write-Host ("    1  unfinished downloads (.part)   {0,3} files  {1}" -f $parts.Count,  (GB $parts.Bytes))
Write-Host ("    2  input   source videos          {0,3} files  {1}" -f $inputs.Count, (GB $inputs.Bytes))
Write-Host ("    3  output  finished + chapters    {0,3} files  {1}" -f $output.Count, (GB $output.Bytes))
Write-Host ("    4  work    leftover render pieces {0,3} files  {1}" -f $pieces.Count, (GB $pieces.Bytes))
Write-Host ("    5  work    all scratch + cache    {0,3} files  {1}" -f $work.Count,   (GB $work.Bytes))
Write-Host ("    6  everything above                          {0}" -f (GB ($parts.Bytes + $inputs.Bytes + $output.Bytes + $work.Bytes)))
Write-Host "    0  cancel"

if ($parts.Count -gt 0) {
    Write-Host ""
    Write-Host "  Note: those .part files are unfinished downloads, not rubbish." -ForegroundColor Yellow
    Write-Host "        Start.cmd with the same link RESUMES from them." -ForegroundColor Yellow
    Write-Host "        Deleting them means downloading from zero again." -ForegroundColor Yellow
}
if ($output.Count -gt 0) {
    Write-Host ""
    Write-Host "  Note: output holds finished videos. Copy anything you want to" -ForegroundColor Yellow
    Write-Host "        keep before clearing it. Clearing output does NOT touch" -ForegroundColor Yellow
    Write-Host "        work\, so pick 4 or 5 as well to reclaim that space." -ForegroundColor Yellow
}
if ($pieces.Count -gt 0) {
    Write-Host ""
    Write-Host ("  Note: {0} of render pieces are sitting in work\. A render" -f (GB $pieces.Bytes).Trim()) -ForegroundColor Yellow
    Write-Host "        that finishes deletes its own, so these are either from" -ForegroundColor Yellow
    Write-Host "        a run that was interrupted -- nothing will ever read" -ForegroundColor Yellow
    Write-Host "        them again -- or from debug.cmd / --parts-only, where" -ForegroundColor Yellow
    Write-Host "        the pieces ARE the result you asked for." -ForegroundColor Yellow
    Write-Host "        Choice 4 removes them and leaves signal.npz alone;" -ForegroundColor Yellow
    Write-Host "        choice 5 also drops the cache, costing a re-analysis." -ForegroundColor Yellow
}

Write-Host ""
$choice = (Read-Host "  Choose").Trim()

$targets = switch ($choice) {
    "1" { @{ Name = "unfinished downloads";  Set = $parts } }
    "2" { @{ Name = "input videos";          Set = $inputs } }
    "3" { @{ Name = "output";                Set = $output } }
    "4" { @{ Name = "leftover render pieces"; Set = $pieces } }
    "5" { @{ Name = "work";                  Set = $work } }
    "6" { @{ Name = "everything";
             Set = (Measure-Set (@(Get-Parts) + @(Get-InputVideos) + @(Get-Output) + @(Get-Work))) } }
    default { $null }
}

if (-not $targets) {
    Write-Host ""
    Write-Host "  Nothing deleted." -ForegroundColor Green
    Write-Host ""
    Read-Host "  Press Enter to close" | Out-Null
    exit 0
}
if ($targets.Set.Count -eq 0) {
    Write-Host ""
    Write-Host "  Nothing there to delete." -ForegroundColor Green
    Write-Host ""
    Read-Host "  Press Enter to close" | Out-Null
    exit 0
}

Line
Write-Host ""
Write-Host ("  About to send {0} file(s), {1}, to the Recycle Bin:" -f `
    $targets.Set.Count, (GB $targets.Set.Bytes))
Write-Host ""
$targets.Set.Files | Select-Object -First 12 | ForEach-Object {
    Write-Host ("    {0,8:N2} GiB  {1}" -f ($_.Length / 1GB), $_.Name)
}
if ($targets.Set.Count -gt 12) {
    Write-Host ("    ... and {0} more" -f ($targets.Set.Count - 12))
}

Write-Host ""
Write-Host "  They go to the Recycle Bin, so this can be undone." -ForegroundColor DarkGray
$confirm = (Read-Host "  Type DELETE to confirm").Trim()
if ($confirm -cne "DELETE") {
    Write-Host ""
    Write-Host "  Cancelled, nothing deleted." -ForegroundColor Green
    Write-Host ""
    Read-Host "  Press Enter to close" | Out-Null
    exit 0
}

$removed = 0
$freed = 0
foreach ($f in $targets.Set.Files) {
    try {
        [Microsoft.VisualBasic.FileIO.FileSystem]::DeleteFile(
            $f.FullName,
            [Microsoft.VisualBasic.FileIO.UIOption]::OnlyErrorDialogs,
            [Microsoft.VisualBasic.FileIO.RecycleOption]::SendToRecycleBin)
        $removed++
        $freed += $f.Length
    } catch {
        Write-Host ("  could not delete {0}: {1}" -f $f.Name, $_.Exception.Message) -ForegroundColor Red
    }
}

# Empty folders left behind under work\ are just noise.
#
# -LiteralPath on BOTH calls. A downloaded folder is named "[DD-MM-YYYY] title
# [videoid]", and a bare path argument reads those brackets as a wildcard
# character class: the emptiness test then errored, returned nothing, and
# judged a folder holding gigabytes to be empty. It only ever escaped deleting
# one because Remove-Item read the same brackets the same way and matched
# nothing -- two bugs cancelling, on a line that uses -Force and so does NOT
# go to the Recycle Bin this script otherwise promises.
if (Test-Path "work") {
    Get-ChildItem "work" -Directory -Recurse -ErrorAction SilentlyContinue |
        Sort-Object FullName -Descending |
        Where-Object { -not (Get-ChildItem -LiteralPath $_.FullName -Recurse -File -ErrorAction SilentlyContinue) } |
        ForEach-Object { Remove-Item -LiteralPath $_.FullName -Recurse -Force -ErrorAction SilentlyContinue }
}

Line
Write-Host ""
Write-Host ("  Deleted {0} file(s), freed {1}." -f $removed, (GB $freed)) -ForegroundColor Green
Write-Host "  They are in the Recycle Bin if you need them back, which means the"
Write-Host "  space is not returned until you empty it." -ForegroundColor DarkGray
Show-Drive
Write-Host ""
Read-Host "  Press Enter to close" | Out-Null
