# Paper Reviewer 快速启动脚本（PowerShell）

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Paper Reviewer 快速启动" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 设置环境变量
$env:GEMINI_API_KEY = "sk-cCWinKy0Gix1aFdSXDMGs8v6wiET53yNDqDG8GTDkoouHKMb"
$env:GEMINI_BASE_URL = "https://www.packyapi.com/v1"

Write-Host "[1/3] 环境变量已设置" -ForegroundColor Green
Write-Host "  API Key: $($env:GEMINI_API_KEY.Substring(0, 15))..."
Write-Host "  Base URL: $env:GEMINI_BASE_URL"
Write-Host ""

# 切换到项目目录
Set-Location $PSScriptRoot

Write-Host "[2/3] 测试集成..." -ForegroundColor Yellow
python test_integration.py
Write-Host ""

Write-Host "[3/3] 准备就绪！" -ForegroundColor Green
Write-Host ""
Write-Host "现在可以运行：" -ForegroundColor Cyan
Write-Host '  python collect.py --arxiv-id "2401.12345" --stop-at-no-html' -ForegroundColor White
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
