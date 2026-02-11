# 文献综述流水线

自动解析学术论文、生成搜索查询、检索相关文献的完整流水线。

## 📋 快速开始

### 安装依赖

```bash
# 安装所有依赖（无需 SDK）
pip install requests python-dateutil tqdm
```

### 配置 MinerU API

**必须设置环境变量：**

```bash
# 设置 MinerU API Token
export MINERU_API_TOKEN='your_api_token'
```

**如何获取 API Token:**
1. 访问 [https://mineru.net](https://mineru.net)
2. 注册/登录账号
3. 在控制台获取你的 API Token

**优势：**
- ✅ 无页数限制（SDK 限制 10 页）
- ✅ 直接 REST API 调用
- ✅ 更灵活的配置

### 使用示例
```bash
# 基本用法
python main.py your_paper.pdf

# 生成 10 条查询，每条返回 15 篇论文
python main.py your_paper.pdf -n 10 -r 15

# 查看帮助
python main.py --help
```

## 📚 详细文档

请查看 [docs](./docs/) 目录下的文档：
- [README.md](./docs/README.md) - 完整使用手册
- [walkthrough.md](./docs/walkthrough.md) - 实现详解

## � 项目结构

```
literature_review/
├── __init__.py                  # 模块初始化
├── pdf_parser_mineru.py         # PDF 解析
├── metadata_extractor.py        # 元数据提取
├── query_generator.py           # 查询生成
├── arxiv_searcher.py            # arXiv 搜索
├── main.py                      # 主流程
├── requirements.txt             # 依赖列表
└── docs/                        # 文档目录
    ├── README.md                # 使用手册
    └── walkthrough.md           # 实现详解
```

## ⚙️ 配置

需要配置 DeepSeek API（位于项目根目录的 `deepseek_api.py`）：
```bash
export DEEPSEEK_API_KEY="your_api_key"
```

## 📝 许可证

本项目基于父项目 paper-reviewer 的许可证。
