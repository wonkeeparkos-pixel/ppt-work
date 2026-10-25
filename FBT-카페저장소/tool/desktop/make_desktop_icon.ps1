# FBT desktop icon maker
# Double-click the .bat next to this file. It creates a desktop shortcut that opens
# the FBT treatment-point finder (claude.ai) with the FBT logo as its icon.
# ASCII only on purpose: Korean text is written as \u escapes so any Windows code page works.

$ErrorActionPreference = 'Stop'
$U = { param($s) [regex]::Unescape($s) }

$url  = 'https://claude.ai/artifact/R8VRU9wPpaumAa7CEH7gwf'
$name = & $U 'FBT \uce58\ub8cc\uc810 \ucc3e\uae30'
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
  } catch { $iconOk = $false; Write-Host (& $U '\ub85c\uace0 \uadf8\ub9bc\uc740 \ub9cc\ub4e4\uc9c0 \ubabb\ud574\uc11c \uae30\ubcf8 \ubaa8\uc591 \uc544\uc774\ucf58\uc73c\ub85c \ub9cc\ub4e4\uc5c8\uc5b4\uc694.'); Write-Host $_.Exception.Message }

  $desk = [Environment]::GetFolderPath('Desktop')
  $file = Join-Path $desk ($name + '.url')
  $lines = @('[InternetShortcut]', "URL=$url")
  if ($iconOk) { $lines += "IconFile=$ico"; $lines += 'IconIndex=0' }
  [System.IO.File]::WriteAllLines($file, [string[]]$lines, [System.Text.Encoding]::Default)

  # ask Explorer to redraw icons (harmless if it does nothing)
  try { Start-Process -FilePath 'ie4uinit.exe' -ArgumentList '-show' -WindowStyle Hidden } catch { }
  Write-Host ''
  Write-Host (& $U '\ubc14\ud0d5\ud654\uba74\uc5d0 \u0027FBT \uce58\ub8cc\uc810 \ucc3e\uae30\u0027 \uc544\uc774\ucf58\uc744 \ub9cc\ub4e4\uc5c8\uc5b4\uc694. \ub354\ube14\ud074\ub9ad\ud558\uba74 \uc5f4\ub824\uc694.')
  Write-Host $file
} catch {
  Write-Host (& $U '\uc544\uc774\ucf58\uc744 \ub9cc\ub4e4\uc9c0 \ubabb\ud588\uc5b4\uc694. \uc544\ub798 \ub0b4\uc6a9\uc744 \ucea1\ucc98\ud574\uc11c \uc54c\ub824\uc8fc\uc138\uc694.')
  Write-Host $_.Exception.Message
  exit 1
}
