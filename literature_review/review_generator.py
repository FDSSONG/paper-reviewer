#!/usr/bin/env python3
"""
评审报告生成模块
基于原始论文和相关文献生成结构化学术评审报告
"""
import sys
import os
from pathlib import Path
from typing import List, Dict, Optional
from literature_review.logger import get_logger

logger = get_logger("review_generator")

# 添加父目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from deepseek_api import DeepSeekAPI


class ReviewGenerator:
    """学术评审报告生成器"""
    
    def __init__(self):
        """初始化生成器"""
        self.api = DeepSeekAPI()
    
    def generate_review(
        self,
        source_paper_md: str,
        source_metadata: Dict,
        related_summaries: List[Dict],
        language: str = "chinese"
    ) -> str:
        """
        生成完整的评审报告
        
        Args:
            source_paper_md: 原始论文的 Markdown 内容
            source_metadata: 原始论文元数据
            related_summaries: 相关文献摘要列表
            language: 输出语言 ('chinese' 或 'english')
        
        Returns:
            评审报告 Markdown 文本
        """
        logger.info("🤖 生成评审报告...")
        logger.info(f"论文: {source_metadata.get('title', '')[:60]}...")
        logger.info(f"相关文献数: {len(related_summaries)}")
        
        # 限制论文长度以节省 token
        max_paper_len = 20000
        if len(source_paper_md) > max_paper_len:
            source_paper_md = source_paper_md[:max_paper_len] + "\n\n... (内容过长已截断)"
        
        # 构建提示词
        if language == "chinese":
            prompt = self._build_chinese_prompt(
                source_paper_md, source_metadata, related_summaries
            )
        else:
            prompt = self._build_english_prompt(
                source_paper_md, source_metadata, related_summaries
            )
        
        try:
            review = self.api.simple_ask(prompt, temperature=0.7)
            logger.info(f"✅ 评审报告生成成功 ({len(review)} 字符)")
            return review
        
        except Exception as e:
            logger.error(f"评审报告生成失败: {e}")
            return self._generate_fallback_review(source_metadata, language)
    
    def _build_chinese_prompt(
        self,
        source_paper_md: str,
        source_metadata: Dict,
        related_summaries: List[Dict]
    ) -> str:
        """构建中文评审提示词"""
        
        # 格式化相关文献
        literature_text = self._format_related_literature(related_summaries, "chinese")
        
        prompt = f"""你是一位经验丰富的学术审稿人，请对以下论文进行全面、客观的评审。

# 原始论文

**标题**: {source_metadata.get('title', '未知')}
**作者**: {', '.join(source_metadata.get('authors', [])[:5])}

**完整内容**:
{source_paper_md}

# 相关文献对比分析

{literature_text}

---

请按照以下结构生成评审报告：

## 1. 主要贡献
用一句话（不超过50词）总结本文的核心贡献。

## 2. 优势 (Strengths)
列出 3-5 条优势，每条需要：
- 清晰的标题
- 详细描述（50-100词）
- 引用支持该优势的相关文献（从上述文献列表中选择，标明 arXiv ID）

格式示例：
**优势1: [标题]**
- 描述: ...
- 支持文献: [2301.12345] 论文标题

## 3. 劣势 (Weaknesses)
列出 3-5 条劣势，每条需要：
- 清晰的标题
- 问题描述（30-50词）
- 具体、可操作的改进建议（30-50词）

格式示例：
**劣势1: [标题]**
- 问题: ...
- 建议: ...

## 4. 具体问题列表

分为三个类别，每类列出 2-5 个具体、可验证的问题：

### 实验相关
- [ ] 问题1: ...（指出具体实验、数据集或指标）
- [ ] 问题2: ...

### 写作相关
- [ ] 问题1: ...（指出具体章节或段落）
- [ ] 问题2: ...

### 引用文献相关
- [ ] 问题1: ...（指出缺失的重要文献或引用不当之处）
- [ ] 问题2: ...

## 5. 详细评分

对以下 7 个维度评分（1-10分），并给出简短说明（20-30词）：

| 维度 | 评分 | 说明 |
|------|------|------|
| 原创性 (Originality) | X/10 | 研究思路的新颖程度... |
| 问题重要性 (Significance) | X/10 | 研究问题对领域的重要性... |
| 结论支持度 (Soundness) | X/10 | 结论是否被实验和理论充分支持... |
| 实验严谨度 (Rigor) | X/10 | 实验设计的严谨性和可复现性... |
| 写作清晰度 (Clarity) | X/10 | 论文表达的清晰程度和逻辑性... |
| 社区价值 (Impact) | X/10 | 对学术社区的潜在影响... |
| 相关工作对比 (Related Work) | X/10 | 与既往工作对比的充分性... |

**总体评分**: X/10

**评分理由**: [一句话说明总体评分的依据]

## 6. 评审总结

用 100-150 词总结评审意见，基于以上分析给出明确的建议：
- **接受 (Accept)**: 论文质量优秀，建议直接接受
- **弱接受 (Weak Accept)**: 论文总体不错，需要小幅修改
- **弱拒绝 (Weak Reject)**: 存在显著问题，需要大幅修改
- **拒绝 (Reject)**: 论文质量不足，建议拒绝

---

要求：
- 客观、专业、建设性
- 基于证据，引用具体章节或文献
- 避免模糊表述，给出可操作建议
- 评分标准：1-3分=不合格，4-6分=一般，7-9分=良好，10分=卓越
- 优势要有文献支持，劣势要有改进建议
"""
        return prompt
    
    def _build_english_prompt(
        self,
        source_paper_md: str,
        source_metadata: Dict,
        related_summaries: List[Dict]
    ) -> str:
        """构建英文评审提示词"""
        
        literature_text = self._format_related_literature(related_summaries, "english")
        
        prompt = f"""You are an experienced academic reviewer. Please provide a comprehensive and objective review of the following paper.

# Original Paper

**Title**: {source_metadata.get('title', 'Unknown')}
**Authors**: {', '.join(source_metadata.get('authors', [])[:5])}

**Full Content**:
{source_paper_md}

# Related Literature Analysis

{literature_text}

---

Please generate a review report following this structure:

## 1. Main Contribution
Summarize the core contribution in one sentence (max 50 words).

## 2. Strengths
List 3-5 strengths, each including:
- Clear title
- Detailed description (50-100 words)
- Supporting citations from the related literature above (with arXiv ID)

Format:
**Strength 1: [Title]**
- Description: ...
- Supporting Literature: [2301.12345] Paper Title

## 3. Weaknesses
List 3-5 weaknesses, each including:
- Clear title
- Problem description (30-50 words)
- Specific, actionable improvement suggestions (30-50 words)

Format:
**Weakness 1: [Title]**
- Issue: ...
- Suggestion: ...

## 4. Specific Issues

Organize into three categories, listing 2-5 concrete, verifiable issues each:

### Experimental Issues
- [ ] Issue 1: ...
- [ ] Issue 2: ...

### Writing Issues
- [ ] Issue 1: ...
- [ ] Issue 2: ...

### Citation Issues
- [ ] Issue 1: ...
- [ ] Issue 2: ...

## 5. Detailed Scores

Score the following 7 dimensions (1-10), with brief explanations (20-30 words):

| Dimension | Score | Explanation |
|-----------|-------|-------------|
| Originality | X/10 | Novelty of the research approach... |
| Significance | X/10 | Importance of the research problem... |
| Soundness | X/10 | How well conclusions are supported... |
| Rigor | X/10 | Rigor of experimental design... |
| Clarity | X/10 | Clarity of writing and presentation... |
| Impact | X/10 | Potential impact on the community... |
| Related Work | X/10 | Completeness of related work comparison... |

**Overall Score**: X/10

**Justification**: [One sentence explaining the overall score]

## 6. Review Summary

Summarize your review in 100-150 words and provide a clear recommendation:
- **Accept**: High quality, recommend acceptance
- **Weak Accept**: Good overall, minor revisions needed
- **Weak Reject**: Significant issues, major revisions required
- **Reject**: Insufficient quality, recommend rejection

---

Requirements:
- Objective, professional, and constructive
- Evidence-based with specific references
- Avoid vague statements, provide actionable suggestions
- Scoring: 1-3=poor, 4-6=fair, 7-9=good, 10=excellent
"""
        return prompt
    
    def _format_related_literature(
        self,
        summaries: List[Dict],
        language: str
    ) -> str:
        """格式化相关文献摘要"""
        content = ""
        
        for i, item in enumerate(summaries, 1):
            score = float(item['score'])
            if language == "chinese":
                content += f"\n## 相关文献 {i}\n"
                content += f"**标题**: {item['title']}\n"
                content += f"**arXiv ID**: {item['arxiv_id']}\n"
                content += f"**相关度**: {score:.3f}\n"
                content += f"**对比摘要**:\n{item['summary']}\n"
            else:
                content += f"\n## Related Paper {i}\n"
                content += f"**Title**: {item['title']}\n"
                content += f"**arXiv ID**: {item['arxiv_id']}\n"
                content += f"**Relevance**: {score:.3f}\n"
                content += f"**Comparative Summary**:\n{item['summary']}\n"
            
            content += "\n---\n"
        
        return content
    
    def _generate_fallback_review(
        self,
        source_metadata: Dict,
        language: str
    ) -> str:
        """生成备用评审（当 LLM 调用失败时）"""
        if language == "chinese":
            return f"""# 评审报告生成失败

由于 API 调用失败，无法生成完整评审报告。
论文：{source_metadata.get('title', '未知')}

请检查：
1. DEEPSEEK_API_KEY 环境变量是否正确设置
2. 网络连接是否正常
3. API 配额是否充足
"""
        else:
            return f"""# Review Generation Failed

Failed to generate complete review due to API error.
Paper: {source_metadata.get('title', 'Unknown')}

Please check:
1. DEEPSEEK_API_KEY environment variable
2. Network connection
3. API quota
"""
    
    def save_review(
        self,
        review: str,
        output_path: Path,
        metadata: Dict = None
    ):
        """
        保存评审报告
        
        Args:
            review: 评审内容
            output_path: 输出文件路径
            metadata: 额外的元数据（可选）
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        content = ""
        
        # 添加元数据头部
        if metadata:
            content += "# 学术论文评审报告\n\n"
            content += "## 📋 基本信息\n\n"
            content += f"- **论文标题**: {metadata.get('title', '')}\n"
            content += f"- **作者**: {', '.join(metadata.get('authors', [])[:5])}\n"
            
            from datetime import datetime
            content += f"- **评审日期**: {datetime.now().strftime('%Y-%m-%d')}\n"
            content += f"- **相关文献数**: {metadata.get('num_related_papers', 0)}\n"
            content += "\n---\n\n"
        
        # 添加评审内容
        content += review
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f"✅ 评审报告已保存: {output_path}")


# 测试代码
if __name__ == "__main__":
    generator = ReviewGenerator()
    
    source_md = """
# Attention Is All You Need

## Abstract
We propose a new simple network architecture, the Transformer...

## 1. Introduction
...

## 2. Model Architecture
...
"""
    
    source_metadata = {
        'title': 'Attention Is All You Need',
        'authors': ['Ashish Vaswani', 'Noam Shazeer'],
        'abstract': 'We propose a new simple network architecture, the Transformer.'
    }
    
    related_summaries = [
        {
            'arxiv_id': '1810.04805',
            'title': 'BERT: Pre-training of Deep Bidirectional Transformers',
            'score': 0.85,
            'summary': '本文在 Transformer 基础上提出了双向预训练方法...'
        }
    ]
    
    review = generator.generate_review(
        source_md,
        source_metadata,
        related_summaries,
        language="chinese"
    )
    
    print("\n生成的评审报告:")
    print("=" * 70)
    print(review)
