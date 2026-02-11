@echo off
REM Paper Reviewer 快速启动脚本（Windows）

echo ========================================
echo Paper Reviewer 快速启动
echo ========================================
echo.

REM 设置环境变量
set GEMINI_API_KEY=sk-cCWinKy0Gix1aFdSXDMGs8v6wiET53yNDqDG8GTDkoouHKMb
set GEMINI_BASE_URL=https://www.packyapi.com/v1

echo [1/3] 环境变量已设置
echo   API Key: %GEMINI_API_KEY:~0,15%...
echo   Base URL: %GEMINI_BASE_URL%
echo.

REM 切换到项目目录
cd /d %~dp0

echo [2/3] 测试集成...
python test_integration.py
echo.

echo [3/3] 准备就绪！
echo.
echo 现在可以运行：
echo   python collect.py --arxiv-id "2401.12345" --stop-at-no-html
echo.
echo ========================================
pause
