# =====================================================
# 智能營銷後台爬蟲 - Windows Task Scheduler 排程設定
# =====================================================
# 用法：以系統管理員權限執行此腳本
#   .\schedule_task.ps1
#   .\schedule_task.ps1 -Time "09:00"
#   .\schedule_task.ps1 -Remove
# =====================================================

param(
    [string]$Time = "09:00",     # 每日執行時間（預設早上 9:00）
    [switch]$Remove              # 移除排程任務
)

$TaskName = "i17Game_MarTech_Scraper"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PythonPath = (Get-Command python -ErrorAction SilentlyContinue).Source
$ScraperPath = Join-Path $ScriptDir "scraper.py"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  智能營銷後台爬蟲 - 排程設定" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 移除排程
if ($Remove) {
    Write-Host "正在移除排程任務 '$TaskName'..." -ForegroundColor Yellow
    try {
        Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction Stop
        Write-Host "✅ 排程任務已移除" -ForegroundColor Green
    } catch {
        Write-Host "⚠️ 排程任務不存在或移除失敗：$_" -ForegroundColor Yellow
    }
    exit 0
}

# 檢查 Python
if (-not $PythonPath) {
    Write-Host "❌ 找不到 Python，請確認已安裝並加入 PATH" -ForegroundColor Red
    exit 1
}
Write-Host "Python 路徑：$PythonPath" -ForegroundColor Gray

# 檢查腳本
if (-not (Test-Path $ScraperPath)) {
    Write-Host "❌ 找不到 scraper.py：$ScraperPath" -ForegroundColor Red
    exit 1
}

# 建立排程任務
Write-Host "正在建立每日 $Time 執行的排程任務..." -ForegroundColor Yellow

$Action = New-ScheduledTaskAction `
    -Execute $PythonPath `
    -Argument "`"$ScraperPath`"" `
    -WorkingDirectory $ScriptDir

$Trigger = New-ScheduledTaskTrigger `
    -Daily `
    -At $Time

$Settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RunOnlyIfNetworkAvailable

try {
    # 若已存在則先移除
    $existing = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
    if ($existing) {
        Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
        Write-Host "  已移除舊的排程任務" -ForegroundColor Gray
    }

    Register-ScheduledTask `
        -TaskName $TaskName `
        -Action $Action `
        -Trigger $Trigger `
        -Settings $Settings `
        -Description "智能營銷後台自動化爬蟲 - 每日擷取每日媒體明細報表" `
        -RunLevel Highest | Out-Null

    Write-Host "" -ForegroundColor Green
    Write-Host "✅ 排程任務已建立！" -ForegroundColor Green
    Write-Host "" -ForegroundColor Green
    Write-Host "  任務名稱：$TaskName" -ForegroundColor White
    Write-Host "  執行時間：每日 $Time" -ForegroundColor White
    Write-Host "  執行腳本：$ScraperPath" -ForegroundColor White
    Write-Host ""
    Write-Host "提示：" -ForegroundColor Yellow
    Write-Host "  - 可在 Task Scheduler 中查看任務狀態" -ForegroundColor Gray
    Write-Host "  - 變更時間：.\schedule_task.ps1 -Time '10:30'" -ForegroundColor Gray
    Write-Host "  - 移除排程：.\schedule_task.ps1 -Remove" -ForegroundColor Gray
    Write-Host "  - ⚠️ 請確保 Session 未過期，否則需重新執行 --login" -ForegroundColor Yellow

} catch {
    Write-Host "❌ 建立排程任務失敗：$_" -ForegroundColor Red
    Write-Host "  請嘗試以系統管理員權限執行此腳本" -ForegroundColor Yellow
    exit 1
}
