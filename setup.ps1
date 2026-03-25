# =====================================================
# 智能營銷後台爬蟲 - 環境安裝腳本
# =====================================================

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  智能營銷後台爬蟲 - 環境安裝" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 安裝 Python 依賴
Write-Host "[1/2] 安裝 Python 套件..." -ForegroundColor Yellow
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Python 套件安裝失敗" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Python 套件安裝完成" -ForegroundColor Green
Write-Host ""

# 安裝 Playwright 瀏覽器
Write-Host "[2/2] 安裝 Playwright Chromium 瀏覽器..." -ForegroundColor Yellow
python -m playwright install chromium
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Playwright 瀏覽器安裝失敗" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Playwright 瀏覽器安裝完成" -ForegroundColor Green
Write-Host ""

# 建立輸出資料夾
$outputDir = "output"
if (-not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir | Out-Null
    Write-Host "✅ 已建立 output/ 資料夾" -ForegroundColor Green
}

$screenshotsDir = "screenshots"
if (-not (Test-Path $screenshotsDir)) {
    New-Item -ItemType Directory -Path $screenshotsDir | Out-Null
    Write-Host "✅ 已建立 screenshots/ 資料夾" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  安裝完成！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "首次使用請先登入：" -ForegroundColor Yellow
Write-Host "  python scraper.py --login" -ForegroundColor White
Write-Host ""
Write-Host "登入後即可執行爬蟲：" -ForegroundColor Yellow
Write-Host "  python scraper.py" -ForegroundColor White
Write-Host ""
