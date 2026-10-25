# FBT desktop icon maker
# Double-click the .bat next to this file. It creates a desktop shortcut that opens
# the FBT treatment-point finder (claude.ai) with the FBT logo as its icon.
# ASCII only on purpose: Korean text is written as character codes so any Windows code page works.

$ErrorActionPreference = 'Stop'
function K([int[]]$c) { -join ($c | ForEach-Object { [char]$_ }) }   # text from character codes

$url  = 'https://claude.ai/artifact/R8VRU9wPpaumAa7CEH7gwf'
$name = (K 0x46,0x42,0x54,0x20,0xce58,0xb8cc,0xc810,0x20,0xcc3e,0xae30)
# icon lives where the path is the same on every PC (a OneDrive-synced desktop shares the .url)
$dir  = Join-Path $env:ProgramData 'FBT'
$ico  = Join-Path $dir 'fbt.ico'

function New-FbtIcon([string]$path) {
  Add-Type -AssemblyName System.Drawing
  $ink = [System.Drawing.Color]::FromArgb(255, 22, 36, 45)
  $pngs = @()
  foreach ($size in 256, 48, 32, 16) {
    $k = $size / 256.0
    $bmp = New-Object System.Drawing.Bitmap($size, $size, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    $g.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
    $g.Clear([System.Drawing.Color]::Transparent)

    # white rounded square behind the mark
    $m = 10 * $k; $w = $size - 2 * $m; $d = 2 * 50 * $k
    $bg = New-Object System.Drawing.Drawing2D.GraphicsPath
    $bg.AddArc($m, $m, $d, $d, 180, 90)
    $bg.AddArc($m + $w - $d, $m, $d, $d, 270, 90)
    $bg.AddArc($m + $w - $d, $m + $w - $d, $d, $d, 0, 90)
    $bg.AddArc($m, $m + $w - $d, $d, $d, 90, 90)
    $bg.CloseFigure()
    $g.FillPath([System.Drawing.Brushes]::White, $bg)

    # FBT mark, same geometry as fbt_icon.svg (units: x 5..49, y 7.5..82)
    $s  = 2.55 * $k
    $ox = 128 * $k - 27 * $s
    $oy = 128 * $k - 44.75 * $s
    $pw = [Math]::Max(5 * $s, 1.4)
    $pen = New-Object System.Drawing.Pen($ink, [single]$pw)
    $body = New-Object System.Drawing.Drawing2D.GraphicsPath
    $body.AddLine([single]($ox + 12 * $s), [single]($oy + 67 * $s), [single]($ox + 12 * $s), [single]($oy + 33 * $s))
    $body.AddArc([single]($ox + 12 * $s), [single]($oy + 18 * $s), [single](30 * $s), [single](30 * $s), 180, 180)
    $body.AddLine([single]($ox + 42 * $s), [single]($oy + 33 * $s), [single]($ox + 42 * $s), [single]($oy + 67 * $s))
    $g.DrawPath($pen, $body)
    $g.DrawEllipse($pen, [single]($ox + 12 * $s), [single]($oy + 52 * $s), [single](30 * $s), [single](30 * $s))
    $g.DrawLine($pen, [single]($ox + 27 * $s), [single]($oy + 7.5 * $s), [single]($ox + 27 * $s), [single]($oy + 82 * $s))
    $g.DrawLine($pen, [single]($ox + 5 * $s), [single]($oy + 44 * $s), [single]($ox + 49 * $s), [single]($oy + 44 * $s))

    $ms = New-Object System.IO.MemoryStream
    $bmp.Save($ms, [System.Drawing.Imaging.ImageFormat]::Png)
    $pngs += ,@($size, $ms.ToArray())
    $pen.Dispose(); $body.Dispose(); $bg.Dispose(); $g.Dispose(); $bmp.Dispose(); $ms.Dispose()
  }

  # .ico container holding the PNG images (supported since Windows Vista)
  $fs = [System.IO.File]::Create($path)
  $bw = New-Object System.IO.BinaryWriter($fs)
  try {
    $bw.Write([UInt16]0); $bw.Write([UInt16]1); $bw.Write([UInt16]$pngs.Count)
    $offset = 6 + 16 * $pngs.Count
    foreach ($p in $pngs) {
      $dim = if ($p[0] -ge 256) { 0 } else { $p[0] }
      $bw.Write([Byte]$dim); $bw.Write([Byte]$dim); $bw.Write([Byte]0); $bw.Write([Byte]0)
      $bw.Write([UInt16]1); $bw.Write([UInt16]32)
      $bw.Write([UInt32]$p[1].Length); $bw.Write([UInt32]$offset)
      $offset += $p[1].Length
    }
    foreach ($p in $pngs) { $bw.Write([byte[]]$p[1]) }
  } finally { $bw.Close() }
}

try {
  $iconOk = $true
  try {
    if (-not (Test-Path $ico)) {
      try { New-Item -ItemType Directory -Force -Path $dir | Out-Null; New-FbtIcon $ico }
      catch {
        # ProgramData not writable here: keep the icon in this user's own folder instead
        $dir = Join-Path $env:LOCALAPPDATA 'FBT'; $ico = Join-Path $dir 'fbt.ico'
        New-Item -ItemType Directory -Force -Path $dir | Out-Null; New-FbtIcon $ico
      }
    }
  } catch { $iconOk = $false; Write-Host ((K 0xb85c,0xace0,0x20,0xadf8,0xb9bc,0xc740,0x20,0xb9cc,0xb4e4,0xc9c0,0x20,0xbabb,0xd574,0xc11c,0x20,0xae30,0xbcf8,0x20,0xbaa8,0xc591,0x20,0xc544,0xc774,0xcf58,0xc73c,0xb85c,0x20,0xb9cc,0xb4e4,0xc5c8,0xc5b4,0xc694,0x2e)); Write-Host $_.Exception.Message }

  $desk = [Environment]::GetFolderPath('Desktop')
  $file = Join-Path $desk ($name + '.url')
  $lines = @('[InternetShortcut]', "URL=$url")
  if ($iconOk) { $lines += "IconFile=$ico"; $lines += 'IconIndex=0' }
  [System.IO.File]::WriteAllLines($file, [string[]]$lines, [System.Text.Encoding]::Default)

  # ask Explorer to redraw icons (harmless if it does nothing)
  try { Start-Process -FilePath 'ie4uinit.exe' -ArgumentList '-show' -WindowStyle Hidden } catch { }
  Write-Host ''
  Write-Host ((K 0xbc14,0xd0d5,0xd654,0xba74,0xc5d0,0x20,0x27,0x46,0x42,0x54,0x20,0xce58,0xb8cc,0xc810,0x20,0xcc3e,0xae30,0x27,0x20,0xc544,0xc774,0xcf58,0xc744,0x20,0xb9cc,0xb4e4,0xc5c8,0xc5b4,0xc694,0x2e,0x20,0xb354,0xbe14,0xd074,0xb9ad,0xd558,0xba74,0x20,0xc5f4,0xb824,0xc694,0x2e))
  Write-Host $file
} catch {
  Write-Host ((K 0xc544,0xc774,0xcf58,0xc744,0x20,0xb9cc,0xb4e4,0xc9c0,0x20,0xbabb,0xd588,0xc5b4,0xc694,0x2e,0x20,0xc544,0xb798,0x20,0xb0b4,0xc6a9,0xc744,0x20,0xcea1,0xcc98,0xd574,0xc11c,0x20,0xc54c,0xb824,0xc8fc,0xc138,0xc694,0x2e))
  Write-Host $_.Exception.Message
  exit 1
}
