# Paper Reviewer 快速启动指南

## 🚀 快速启动（3步）

### 第 1 步：设置环境变量

打开 CMD（命令提示符），运行：

```cmd
:: 设置 API 密钥
set GEMINI_API_KEY=sk-cCWinKy0Gix1aFdSXDMGs8v6wiET53yNDqDG8GTDkoouHKMb

:: 设置中转站地址
set GEMINI_BASE_URL=https://www.packyapi.com/v1

:: 验证设置
echo API Key: %GEMINI_API_KEY%
echo Base URL: %GEMINI_BASE_URL%
```

### 第 2 步：安装依赖（首次运行）

```bash
cd e:\Project\paper-reviewer
pip install -r requirements.txt
```

### 第 3 步：运行项目

#### 方式 A：使用启动脚本（最简单 ⭐推荐）
```cmd
:: 直接双击运行
start.bat

:: 或在 CMD 中运行
cd /d e:\Project\paper-reviewer
start.bat
```

#### 方式 B：手动运行测试
```cmd
python test_integration.py
```

**预期输出：**
```
✅ 使用中转站 API: https://www.packyapi.com/v1
   API Key: sk-cCWinKy...
✅ config_api 模块导入成功
✅ 所有 pipeline 模块导入成功
```

#### 方式 C：处理一篇论文（完整流程）
```cmd
:: 最简单的方式（仅处理有 HTML 版本的论文）
python collect.py --arxiv-id "2401.12345" --stop-at-no-html

:: 或使用具体的 arXiv ID（替换为实际 ID）
python collect.py --arxiv-id "2312.00752" --stop-at-no-html
```

---

## 📋 详细说明

### 环境变量说明

| 变量名 | 值 | 说明 |
|-------|-----|------|
| `GEMINI_API_KEY` | sk-cCWinKy... | 你的中转站 API 密钥 |
| `GEMINI_BASE_URL` | https://www.packyapi.com/v1 | 中转站地址 |

**⚠️ 注意：** 环境变量只在当前 CMD 窗口有效。如果关闭窗口，需要重新设置。

**💡 提示：** 推荐使用 `start.bat` 脚本，它会自动设置环境变量。

### 命令行参数说明

```bash
python collect.py [选项]

必选参数（二选一）：
  --arxiv-id ID          arXiv 论文 ID（如 2401.12345）
  --openreview-id ID     OpenReview 论文 ID

可选参数：
  --stop-at-no-html              如果没有 HTML 版本则跳过（推荐，节省成本）
  --workers N                    并发数（默认 10）
  --skip-page-threshold N        跳过超过 N 页的论文（默认 50）
  --use-upstage                  使用 Upstage 提取图表（需要额外 API key）
  --use-mineru                   使用 MinerU 提取图表（需要 Python 3.10）
  --voice-synthesis vertexai     生成播客音频
```

### 常用命令示例

```cmd
:: 1. 最简单：只处理有 HTML 的论文
python collect.py --arxiv-id "2401.12345" --stop-at-no-html

:: 2. 设置更高并发
python collect.py --arxiv-id "2401.12345" --workers 20

:: 3. 限制论文页数
python collect.py --arxiv-id "2401.12345" --skip-page-threshold 30

:: 4. 处理 OpenReview 论文
python collect.py --openreview-id "abc123xyz"
```

---

## 🧪 测试步骤

### 1. 测试 API 连接
```bash
python test_integration.py
```

### 2. 快速测试（找一篇简单的论文）
```bash
# 使用一个已知有 HTML 版本的论文
python collect.py --arxiv-id "2312.00752" --stop-at-no-html
```

### 3. 检查输出
```bash
# 成功会生成如下目录结构：
2312.00752/
├── paper.pdf
├── figures.json
├── tables.json
├── essential.json
├── sections.json
└── references.json
```

---

## ❌ 常见问题

### 问题 1：环境变量未设置
**错误信息：**
```
❌ 未设置 GEMINI_API_KEY 环境变量
```

**解决方法：**
```cmd
set GEMINI_API_KEY=your-key
set GEMINI_BASE_URL=https://www.packyapi.com/v1
```

或直接运行 `start.bat` 脚本。

### 问题 2：模块导入失败
**错误信息：**
```
ModuleNotFoundError: No module named 'xxx'
```

**解决方法：**
```bash
pip install -r requirements.txt
```

### 问题 3：API 调用失败
**可能原因：**
- 中转站不支持 `gemini-3-pro-preview` 模型
- API key 错误
- 网络问题

**检查方法：**
```bash
# 查看中转站文档，确认支持的模型
# 或联系中转站客服
```

### 问题 4：找不到 poppler
**错误信息：**
```
pdf2image requires poppler
```

**解决方法（Windows）：**
```bash
# 下载 poppler：https://github.com/oschwartz10612/poppler-windows/releases/
# 解压后添加 bin 目录到系统 PATH
```

---

## 🎯 推荐工作流

### 首次运行
```cmd
:: 1. 进入项目目录
cd /d e:\Project\paper-reviewer

:: 2. 运行启动脚本（自动设置环境变量）
start.bat

:: 3. 安装依赖（如果需要）
pip install -r requirements.txt

:: 4. 运行一个简单测试
python collect.py --arxiv-id "2312.00752" --stop-at-no-html
```

### 日常使用

**方式1：使用启动脚本（推荐）**
```cmd
:: 双击运行 start.bat，然后：
python collect.py --arxiv-id "YOUR_ARXIV_ID" --stop-at-no-html
```

**方式2：手动设置**
```cmd
:: 每次打开新的 CMD 窗口时：
cd /d e:\Project\paper-reviewer
set GEMINI_API_KEY=sk-...
set GEMINI_BASE_URL=https://www.packyapi.com/v1

:: 然后运行项目
python collect.py --arxiv-id "YOUR_ARXIV_ID" --stop-at-no-html
```

---

## 💡 进阶技巧

### 方法1：创建运行脚本（推荐 ⭐）

创建 `run.bat` 文件，每次运行更方便：

```cmd
@echo off
set GEMINI_API_KEY=sk-cCWinKy0Gix1aFdSXDMGs8v6wiET53yNDqDG8GTDkoouHKMb
set GEMINI_BASE_URL=https://www.packyapi.com/v1

echo 请输入 arXiv ID (例如: 2312.00752):
set /p ARXIV_ID=

python collect.py --arxiv-id "%ARXIV_ID%" --stop-at-no-html
pause
```

双击 `run.bat`，输入 arXiv ID 即可自动运行！

### 方法2：永久设置系统环境变量

**通过图形界面设置：**
1. 按 `Win + R`，输入 `sysdm.cpl`
2. 点击"高级" → "环境变量"
3. 在"用户变量"中点击"新建"
4. 添加：
   - 变量名：`GEMINI_API_KEY`
   - 变量值：`sk-cCWinKy0Gix1aFdSXDMGs8v6wiET53yNDqDG8GTDkoouHKMb`
5. 再添加：
   - 变量名：`GEMINI_BASE_URL`
   - 变量值：`https://www.packyapi.com/v1`
6. 点击"确定"，重启 CMD 生效

**通过命令行设置：**
```cmd
setx GEMINI_API_KEY "sk-cCWinKy0Gix1aFdSXDMGs8v6wiET53yNDqDG8GTDkoouHKMb"
setx GEMINI_BASE_URL "https://www.packyapi.com/v1"
```

⚠️ 需要重新打开 CMD 窗口才能生效。

---

## 📞 需要帮助？

如果遇到问题：
1. 检查环境变量是否正确设置
2. 查看错误信息
3. 确认中转站支持 `gemini-3-pro-preview` 模型
4. 告诉我具体的错误信息，我会帮你解决
