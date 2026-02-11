#!/usr/bin/env python3
"""
摘要生成模块
为高相关度论文生成详细对比摘要，为低相关度论文使用原摘要
"""
import sys
import os
from pathlib import Path
from typing import Dict, Optional
from literature_review.logger import get_logger

logger = get_logger("summary_generator")

# 添加父目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from deepseek_api import DeepSeekAPI


class SummaryGenerator:
    """摘要生成器"""
    
    def __init__(self):
        """初始化生成器"""
        self.api = DeepSeekAPI()
    
    def generate_detailed_summary(
        self,
        source_paper: Dict,
        candidate_paper: Dict,
        candidate_markdown: str,
        language: str = "chinese"
    ) -> str:
        """
        为高相关度论文生成详细对比摘要
        
        Args:
            source_paper: 源论文元数据
            candidate_paper: 候选论文元数据
            candidate_markdown: 候选论文的完整 Markdown 内容
            language: 输出语言 ('chinese' 或 'english')
        
        Returns:
            详细摘要文本（200-300词）
        """
        logger.info(f"🤖 生成详细摘要: {candidate_paper['title'][:60]}...")
        
        # 构建提示词
        if language == "chinese":
            prompt = self._build_chinese_prompt(
                source_paper, candidate_paper, candidate_markdown
            )
        else:
            prompt = self._build_english_prompt(
                source_paper, candidate_paper, candidate_markdown
            )
        
        try:
            summary = self.api.simple_ask(prompt, temperature=0.7)
            logger.info(f"✅ 摘要生成成功 ({len(summary)} 字符)")
            return summary
        
        except Exception as e:
            logger.error(f"摘要生成失败: {e}")
            # 降级：返回原摘要
            return candidate_paper.get('abstract', '无摘要')
    
    def _build_chinese_prompt(
        self,
        source_paper: Dict,
        candidate_paper: Dict,
        candidate_markdown: str
    ) -> str:
        """构建中文提示词"""
        source_title = source_paper.get('title', '未知')
        source_abstract = source_paper.get('abstract', '无摘要')
        
        candidate_title = candidate_paper['title']
        candidate_abstract = candidate_paper.get('abstract', '无摘要')
        
        # 限制 Markdown 长度以节省 token
        max_md_len = 15000  # 约 4000 tokens
        if len(candidate_markdown) > max_md_len:
            candidate_markdown = candidate_markdown[:max_md_len] + "\n\n... (内容过长已截断)"
        
        prompt = f"""作为学术研究助手，请对比分析以下两篇论文，写一篇200-300词的中文详细摘要。

【源论文（待研究）】
标题：{source_title}
摘要：{source_abstract}

【候选论文（相关文献）】
标题：{candidate_title}
摘要：{candidate_abstract}

【候选论文完整内容】
{candidate_markdown}

---

请从以下三个焦点进行对比分析：

1. **方法对比**：
   - 两篇论文使用的核心技术方法有何异同？
   - 候选论文的方法是否对源论文有借鉴或改进？
   - 是否采用了不同的技术路线？

2. **实验差异**：
   - 实验设置（数据集、baseline、评估指标）有何不同？
   - 实验结果的对比如何？哪篇表现更好？
   - 是否在相同或不同的应用场景下验证？

3. **结论异同**：
   - 两篇论文的主要研究结论是否一致？
   - 是否存在互补关系或矛盾之处？
   - 候选论文对源论文的研究有何启发或补充？

**要求**：
- 200-300词的中文
- 客观、准确、专业
- 重点突出三个焦点的对比分析
- 不要简单复述论文内容，要深入分析异同
"""
        return prompt
    
    def _build_english_prompt(
        self,
        source_paper: Dict,
        candidate_paper: Dict,
        candidate_markdown: str
    ) -> str:
        """构建英文提示词"""
        source_title = source_paper.get('title', 'Unknown')
        source_abstract = source_paper.get('abstract', 'No abstract')
        
        candidate_title = candidate_paper['title']
        candidate_abstract = candidate_paper.get('abstract', 'No abstract')
        
        # 限制 Markdown 长度
        max_md_len = 15000
        if len(candidate_markdown) > max_md_len:
            candidate_markdown = candidate_markdown[:max_md_len] + "\n\n... (content truncated)"
        
        prompt = f"""As an academic research assistant, please write a detailed 200-300 word comparative summary of the following two papers.

【Source Paper (Under Study)】
Title: {source_title}
Abstract: {source_abstract}

【Candidate Paper (Related Literature)】
Title: {candidate_title}
Abstract: {candidate_abstract}

【Full Content of Candidate Paper】
{candidate_markdown}

---

Please analyze and compare from the following three perspectives:

1. **Methodology Comparison**:
   - What are the similarities and differences in the core technical methods used?
   - Does the candidate paper build upon or improve the source paper's methods?
   - Are different technical approaches employed?

2. **Experimental Differences**:
   - How do the experimental setups (datasets, baselines, evaluation metrics) differ?
   - How do the experimental results compare? Which performs better?
   - Are they validated in the same or different application scenarios?

3. **Conclusion Alignment**:
   - Are the main research conclusions consistent between the two papers?
   - Is there a complementary relationship or contradictions?
   - What insights or supplements does the candidate paper provide for the source paper?

**Requirements**:
- 200-300 words in English
- Objective, accurate, and professional
- Focus on comparative analysis across the three perspectives
- Provide deep analysis of similarities and differences, not just summary
"""
        return prompt
    
    def use_original_abstract(self, paper: Dict) -> str:
        """
        使用原始摘要（低相关度论文）
        
        Args:
            paper: 论文元数据
        
        Returns:
            原始摘要
        """
        abstract = paper.get('abstract', '无摘要')
        logger.info(f"📄 使用原摘要: {paper['title'][:60]}...")
        return abstract
    
    def save_summary(
        self,
        summary: str,
        output_path: Path,
        metadata: Dict = None
    ):
        """
        保存摘要到文件
        
        Args:
            summary: 摘要内容
            output_path: 输出文件路径
            metadata: 额外的元数据（可选）
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        content = ""
        
        # 添加元数据头部
        if metadata:
            content += "---\n"
            content += f"标题: {metadata.get('title', '')}\n"
            content += f"作者: {', '.join(metadata.get('authors', [])[:5])}\n"
            content += f"发布日期: {metadata.get('published', '')}\n"
            content += f"arXiv ID: {metadata.get('arxiv_id', '')}\n"
            content += f"PDF: {metadata.get('pdf_url', '')}\n"
            content += "---\n\n"
        
        # 添加摘要内容
        content += "# 对比摘要\n\n"
        content += summary
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f"✅ 摘要已保存: {output_path}")


# 测试代码
if __name__ == "__main__":
    generator = SummaryGenerator()
    
    source = {
        'title': 'Attention Is All You Need',
        'abstract': 'We propose a new simple network architecture, the Transformer.'
    }
    
    candidate = {
        'arxiv_id': '1810.04805',
        'title': 'BERT: Pre-training of Deep Bidirectional Transformers',
        'abstract': 'We introduce BERT, which stands for Bidirectional Encoder Representations from Transformers.',
        'authors': ['Jacob Devlin', 'Ming-Wei Chang'],
        'published': '2018-10-11',
        'pdf_url': 'https://arxiv.org/pdf/1810.04805'
    }
    
    candidate_md = """
# BERT: Pre-training of Deep Bidirectional Transformers

## Abstract
We introduce a new language representation model called BERT...

## 1. Introduction
Language model pre-training has been shown to be effective...

## 2. Related Work
There is a long history of pre-training general language representations...

## 3. BERT
We introduce BERT and its detailed implementation...
"""
    
    print("=" * 70)
    print("摘要生成测试")
    print("=" * 70)
    
    # 生成详细摘要
    summary = generator.generate_detailed_summary(
        source, candidate, candidate_md, language="chinese"
    )
    
    print("\n生成的摘要:")
    print("-" * 70)
    print(summary)
