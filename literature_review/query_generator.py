#!/usr/bin/env python3
"""
搜索查询生成模块 - 类封装版本
使用 DeepSeek API 从论文内容生成多个搜索查询
"""
import sys
import os
from typing import List, Dict
from literature_review.logger import get_logger

logger = get_logger("query_generator")

# 添加父目录到路径以导入 deepseek_api
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from deepseek_api import DeepSeekAPI


class QueryGenerator:
    """查询生成器类"""
    
    def __init__(self):
        """初始化生成器"""
        self.api = DeepSeekAPI()
    
    def generate_queries(
        self,
        markdown_text: str = None,
        metadata: Dict = None,
        num_queries: int = 7
    ) -> List[str]:
        """
        生成搜索查询（简化版，只返回查询字符串列表）
        
        Args:
            markdown_text: Markdown 文本（可选）
            metadata: 元数据字典（可选，如果提供则使用其中的信息）
            num_queries: 生成的查询数量
        
        Returns:
            ["query1", "query2", ...]
        """
        # 从 metadata 提取信息
        if metadata:
            title = metadata.get('title', '')
            abstract = metadata.get('abstract', '')
            sections = metadata.get('sections', [])
        else:
            title = ''
            abstract = ''
            sections = []
        
        # 调用完整的生成函数
        queries_with_meta = self.generate_search_queries(
            title=title,
            abstract=abstract,
            sections=sections,
            num_queries=num_queries
        )
        
        # 只返回查询字符串
        return [q['query'] for q in queries_with_meta]
    
    def generate_search_queries(
        self,
        title: str,
        abstract: str,
        sections: List[Dict],
        num_queries: int = 7
    ) -> List[Dict[str, str]]:
        """
        生成搜索查询（完整版，包含元信息）
        
        Args:
            title: 论文标题
            abstract: 摘要
            sections: 章节列表
            num_queries: 生成的查询数量（默认7条）
        
        Returns:
            [
                {
                    "query": "deep learning transformers attention mechanism",
                    "perspective": "technical_approach",
                    "description": "相似技术路线"
                },
                ...
            ]
        """
        logger.info(f"🔍 生成 {num_queries} 条搜索查询...")
        
        # 准备论文概要
        section_titles = [s['title'] for s in sections[:10]]  # 只取前10个章节标题
        sections_text = ", ".join(section_titles)
        
        # 构建提示词
        prompt = f"""你是一位学术研究助手。请阅读以下论文信息，生成 {num_queries} 条英文搜索查询，用于在 arXiv 上检索相关论文。

论文标题：{title}

摘要：{abstract if abstract else "无摘要"}

主要章节：{sections_text}

请从以下不同视角生成搜索查询：
1. 相同研究问题（2条）- 研究同一问题的其他方法
2. 相似技术路线（2条）- 使用相同或类似技术的论文
3. 相关标准/基准（1条）- 相关的评估标准、数据集或基准
4. 替代方法（1条）- 解决同一问题的不同方法
5. 应用领域扩展（1条）- 在相关领域的应用

要求：
- 每条查询为3-6个关键词的组合，用空格分隔
- 使用英文，适合 arXiv 搜索
- 避免过于宽泛或过于具体
- 不要包含引号、括号等特殊符号

请以JSON格式返回，格式如下：
{{
  "queries": [
    {{
      "query": "关键词组合",
      "perspective": "research_problem|technical_approach|standard|alternative|application",
      "description": "中文描述这条查询的目的"
    }}
  ]
}}"""
        
        try:
            result = self.api.simple_ask_json(prompt, temperature=0.7)
            
            queries = result.get('queries', [])
            
            # 验证和格式化
            formatted_queries = []
            for q in queries[:num_queries]:
                if 'query' in q and 'perspective' in q:
                    formatted_queries.append({
                        'query': q['query'].strip(),
                        'perspective': q.get('perspective', 'unknown'),
                        'description': q.get('description', '')
                    })
            
            logger.info(f"✅ 成功生成 {len(formatted_queries)} 条查询")
            for i, q in enumerate(formatted_queries, 1):
                logger.info(f"  {i}. [{q['perspective']}] {q['query']}")
            
            return formatted_queries
        
        except Exception as e:
            logger.error(f"生成查询失败: {e}")
            # 返回降级查询（基于标题的简单查询）
            logger.warning("使用降级方案：基于标题生成基础查询")
            return [{
                'query': title.lower().replace(':', '').replace('-', ' ')[:100],
                'perspective': 'title_based',
                'description': '基于标题的基础查询'
            }]


# 为了向后兼容，保留原有的函数接口
def generate_queries_from_metadata(metadata: Dict, num_queries: int = 7) -> List[Dict[str, str]]:
    """向后兼容的函数接口"""
    generator = QueryGenerator()
    return generator.generate_search_queries(
        title=metadata.get('title', ''),
        abstract=metadata.get('abstract', ''),
        sections=metadata.get('sections', []),
        num_queries=num_queries
    )


# 测试代码
if __name__ == "__main__":
    import json
    
    # 示例元数据
    sample_metadata = {
        "title": "Attention Is All You Need: Transformers for Natural Language Processing",
        "abstract": "This paper introduces the Transformer architecture, a novel neural network design that relies entirely on attention mechanisms, dispensing with recurrence and convolutions. We show that Transformers achieve state-of-the-art results on machine translation tasks while being more parallelizable and requiring significantly less time to train.",
        "sections": [
            {"title": "Introduction", "level": 1},
            {"title": "Background", "level": 1},
            {"title": "Model Architecture", "level": 1},
            {"title": "Self-Attention", "level": 2},
            {"title": "Multi-Head Attention", "level": 2},
            {"title": "Experiments", "level": 1},
            {"title": "Results", "level": 1},
            {"title": "Conclusion", "level": 1},
        ]
    }
    
    print("=" * 60)
    print("查询生成测试")
    print("=" * 60)
    
    generator = QueryGenerator()
    queries = generator.generate_queries(metadata=sample_metadata, num_queries=7)
    
    print("\n生成的查询：")
    print(json.dumps(queries, ensure_ascii=False, indent=2))
