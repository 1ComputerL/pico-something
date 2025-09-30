# pico-something-download.ps1
# download pico-something as a zip into Downloads and unzip it

$zipUrl = "https://github.com/1computerl/pico-something/archive/refs/heads/main.zip"
$downloads = [Environment]::GetFolderPath('UserProfile') + "\Downloads"
$zipPath = Join-Path $downloads "pico-something.zip"
$extractPath = Join-Path $downloads "pico-something"

Write-Host "📥 downloading pico-something from $zipUrl ..."

Invoke-WebRequest -Uri $zipUrl -OutFile $zipPath

Write-Host "📂 extracting to $extractPath ..."
if (Test-Path $extractPath) {
    Remove-Item $extractPath -Recurse -Force
}

Expand-Archive -LiteralPath $zipPath -DestinationPath $downloads -Force

# the zip unpacks to pico-something-main by default
$unpacked = Join-Path $downloads "pico-something-main"
Rename-Item -Path $unpacked -NewName "pico-something" -Force

Write-Host "✅ done! pico-something downloaded to $extractPath"
