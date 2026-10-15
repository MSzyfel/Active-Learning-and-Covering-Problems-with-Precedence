param(
    [switch]$LowQuality,
    [switch]$Preview,
    [int]$FPS = 30
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Python = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
$Manim = Join-Path $ProjectRoot ".venv\Scripts\manimgl.exe"
$Config = Join-Path $ProjectRoot "custom_config.yml"
$CacheDir = Join-Path $ProjectRoot ".cache\manim"
$MatplotlibDir = Join-Path $ProjectRoot ".cache\matplotlib"
$FfmpegBinDir = Join-Path $ProjectRoot ".cache\bin"
$FfmpegAlias = Join-Path $FfmpegBinDir "ffmpeg.exe"

New-Item -ItemType Directory -Force -Path $CacheDir, $MatplotlibDir, $FfmpegBinDir | Out-Null
$env:MPLCONFIGDIR = $MatplotlibDir
$Ffmpeg = & $Python -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())"
$Ffmpeg = $Ffmpeg.Trim().Replace("\", "/")
if (-not (Test-Path $FfmpegAlias)) {
    New-Item -ItemType HardLink -Path $FfmpegAlias -Target $Ffmpeg | Out-Null
}
$env:PATH = "$FfmpegBinDir;$env:PATH"

 $ConfigText = @"
directories:
  base: "$($ProjectRoot.Replace('\', '/'))/output/manim"
  cache: "$($CacheDir.Replace('\', '/'))"
file_writer:
  ffmpeg_bin: "$Ffmpeg"
camera:
  fps: $FPS
"@
[System.IO.File]::WriteAllText($Config, $ConfigText, [System.Text.UTF8Encoding]::new($false))

$Arguments = @((Join-Path $ProjectRoot "src\video.py"), "ArticleVideo", "-w")
if ($LowQuality) { $Arguments += "-l" }
if ($Preview) { $Arguments += "-n", "0,2" }
Push-Location $ProjectRoot
& $Manim @Arguments
Pop-Location
exit $LASTEXITCODE
