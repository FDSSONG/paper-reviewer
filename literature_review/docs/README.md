# 文献综述流水线

自动解析学术论文、生成搜索查询、检索相关文献的完整流水线。

## ✨ 功能特性

1. **PDF 解析** - 使用 MinerU 将 PDF 转换为纯文本 Markdown
2. **元数据提取** - 自动提取标题、作者、摘要、章节结构
3. **智能查询生成** - 使用 AI 生成 5-10 条多角度搜索查询
4. **文献检索** - 从 arXiv 批量获取 2020 年后的相关论文
5. **结果导出** - 支持 JSON 和 CSV 格式

## 📋 依赖要求

```bash
# 核心依赖
pip install magic-pdf  # MinerU
pip install requests   # API 调用

# Python 版本要求
python >= 3.10  # MinerU 要求
```

## 🚀 快速开始

### 基本用法

```bash
# 解析论文并检索相关文献
python main.py your_paper.pdf

# 指定输出目录
python main.py your_paper.pdf -o ./output

# 生成 10 条查询，每条返回 15 篇论文
python main.py your_paper.pdf -n 10 -r 15

# 只解析论文，不搜索
python main.py your_paper.pdf --skip-search
```

### 命令行参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `pdf_path` | PDF 文件路径（必需） | - |
| `-o, --output-dir` | 输出目录 | PDF 同目录 |
| `-n, --num-queries` | 生成查询数量 | 7 |
| `-r, --results-per-query` | 每个查询最大结果数 | 10 |
| `-y, --start-year` | 论文起始年份 | 2020 |
| `--skip-search` | 跳过 arXiv 搜索 | - |
| `--format` | 输出格式 (json/csv/both) | both |

## 📂 输出文件

执行完成后会生成以下文件：

```
output/
├── paper_content.md          # 论文 Markdown 文本
├── content_list.json         # MinerU 原始内容列表
├── metadata.json             # 提取的元数据
├── search_queries.json       # 生成的搜索查询
├── related_papers.json       # 相关论文（JSON 格式）
└── related_papers.csv        # 相关论文（CSV 格式）
```

## 📊 输出示例

### metadata.json
```json
{
  "title": "Attention Is All You Need",
  "authors": ["Ashish Vaswani", "Noam Shazeer"],
  "abstract": "The dominant sequence transduction models...",
  "sections": [
    {"title": "Introduction", "level": 1},
    {"title": "Model Architecture", "level": 1}
  ],
  "validation": {
    "is_valid": true,
    "missing_fields": []
  }
}
```

### search_queries.json
```json
[
  {
    "query": "transformer attention mechanism neural networks",
    "perspective": "technical_approach",
    "description": "相似技术路线"
  },
  {
    "query": "sequence to sequence models NLP",
    "perspective": "research_problem",
    "description": "相同研究问题"
  }
]
```

### related_papers.json
```json
[
  {
    "id": "2301.12345",
    "title": "BERT: Pre-training of Deep Bidirectional Transformers",
    "authors": ["Jacob Devlin", "Ming-Wei Chang"],
    "abstract": "We introduce a new language representation model...",
    "published": "2023-01-15",
    "categories": ["cs.CL", "cs.AI"],
    "arxiv_url": "https://arxiv.org/abs/2301.12345",
    "pdf_url": "https://arxiv.org/pdf/2301.12345.pdf",
    "source_query": "transformer attention mechanism"
  }
]
```

## 🔧 模块说明

### 1. pdf_parser_mineru.py
使用 MinerU 解析 PDF 为纯文本 Markdown

```python
from pdf_parser_mineru import parse_pdf_to_markdown

result = parse_pdf_to_markdown("paper.pdf", "output/")
print(result['markdown'])
```

### 2. metadata_extractor.py
从 Markdown 提取元数据并验证

```python
from metadata_extractor import extract_metadata

metadata = extract_metadata(markdown_text)
print(f"标题: {metadata['title']}")
print(f"作者: {metadata['authors']}")
```

### 3. query_generator.py
使用 AI 生成搜索查询（需要配置 DeepSeek API）

```python
from query_generator import generate_queries_from_metadata

queries = generate_queries_from_metadata(metadata, num_queries=7)
for q in queries:
    print(f"{q['query']} [{q['perspective']}]")
```

### 4. arxiv_searcher.py
搜索 arXiv 并批量获取论文元数据

```python
from arxiv_searcher import search_and_deduplicate

papers = search_and_deduplicate(queries, max_results_per_query=10, start_year=2020)
print(f"找到 {len(papers)} 篇相关论文")
```

## ⚙️ 配置

### DeepSeek API 配置
查询生成模块需要 DeepSeek API，请在项目根目录的 `deepseek_api.py` 中配置：

```python
# 或设置环境变量
export DEEPSEEK_API_KEY="your_api_key"
export DEEPSEEK_BASE_URL="https://ark.cn-beijing.volces.com/api/v3/"
export DEEPSEEK_MODEL="deepseek-v3-250324"
```

### MinerU GPU 加速
编辑 `~/magic-pdf.json`：
```json
{
  "device-mode": "cuda"  // 使用 GPU
}
```

## 🐛 故障排除

### 问题：MinerU 解析失败
- 确保 Python 版本为 3.10
- 检查 PDF 文件是否损坏

### 问题：查询生成失败
- 检查 DeepSeek API 配置
- 查看网络连接

### 问题：arXiv 搜索速率限制
- 减少 `--results-per-query` 参数
- 增加查询间延迟（修改 `arxiv_searcher.py` 中的 `delay` 参数）

## 📝 使用示例

### 示例 1：完整流程
```bash
python main.py papers/transformer.pdf -n 8 -r 12 -y 2021
```

### 示例 2：只提取元数据
```bash
python main.py papers/bert.pdf --skip-search
```

### 示例 3：只导出 JSON
```bash
python main.py papers/gpt.pdf --format json
```

## 📜 许可证

本项目基于父项目 paper-reviewer 的许可证。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！
