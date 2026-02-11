#!/bin/bash
# Paper Reviewer 快速启动脚本（Linux/WSL）

echo "========================================"
echo "Paper Reviewer 快速启动"
echo "========================================"
echo ""

# 设置环境变量
export GEMINI_API_KEY="sk-cCWinKy0Gix1aFdSXDMGs8v6wiET53yNDqDG8GTDkoouHKMb"
export GEMINI_BASE_URL="https://www.packyapi.com/v1"

echo "[1/3] 环境变量已设置"
echo "  API Key: ${GEMINI_API_KEY:0:15}..."
echo "  Base URL: $GEMINI_BASE_URL"
echo ""

echo "[2/3] 测试集成..."
python test_integration.py
echo ""

echo "[3/3] 准备就绪！"
echo ""
echo "现在可以运行："
echo '  python collect.py --arxiv-id "2401.12345" --stop-at-no-html'
echo ""
echo "========================================"
