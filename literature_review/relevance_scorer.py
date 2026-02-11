#!/usr/bin/env python3
"""
相关度评分模块
使用轻量级 embedding 模型计算论文之间的相关度
"""
import json
import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple
from sentence_transformers import SentenceTransformer
from literature_review.logger import get_logger

logger = get_logger("relevance_scorer")


class RelevanceScorer:
    """相关度评分器"""
    
    def __init__(self, model_name: str = "shibing624/text2vec-base-chinese"):
        """
        初始化评分器
        
        Args:
            model_name: embedding 模型名称
        """
        logger.info(f"📊 加载 embedding 模型: {model_name}...")
        self.model = SentenceTransformer(model_name)
        logger.info("✅ 模型加载完成")
    
    def compute_embedding(self, text: str, normalize: bool = True) -> np.ndarray:
        """
        计算文本的 embedding
        
        Args:
            text: 输入文本
            normalize: 是否归一化（归一化后点积=余弦相似度）
        
        Returns:
            embedding 向量
        """
        return self.model.encode(text, normalize_embeddings=normalize, convert_to_tensor=False)
    
    def compute_similarity(self, emb1: np.ndarray, emb2: np.ndarray) -> float:
        """
        计算两个 embedding 的余弦相似度
        
        Args:
            emb1: 第一个 embedding（归一化后）
            emb2: 第二个 embedding（归一化后）
        
        Returns:
            相似度分数 (0-1)
        """
        # 归一化后，点积就是余弦相似度
        return float(np.dot(emb1, emb2))
    
    def prepare_paper_text(self, paper: Dict) -> str:
        """
        准备论文文本用于 embedding
        
        Args:
            paper: 论文元数据字典
        
        Returns:
            组合的文本
        """
        # 组合标题和摘要（摘要权重更高）
        title = paper.get('title', '')
        abstract = paper.get('abstract', '')
        
        # 标题重复2次以增加权重
        text = f"{title} {title} {abstract}"
        return text
    
    def score_papers(
        self,
        source_paper: Dict,
        candidate_papers: List[Dict],
        batch_size: int = 32
    ) -> List[Tuple[Dict, float]]:
        """
        为候选论文计算相关度分数
        
        Args:
            source_paper: 源论文元数据
            candidate_papers: 候选论文列表
            batch_size: 批处理大小
        
        Returns:
            [(论文, 相关度分数), ...] 按分数降序排列
        """
        logger.info(f"🔍 计算相关度分数...")
        logger.info(f"源论文: {source_paper.get('title', 'Unknown')[:60]}...")
        logger.info(f"候选论文数: {len(candidate_papers)}")
        
        # 计算源论文的 embedding
        source_text = self.prepare_paper_text(source_paper)
        source_emb = self.compute_embedding(source_text)
        
        # 批量计算候选论文的 embedding（归一化）
        candidate_texts = [self.prepare_paper_text(p) for p in candidate_papers]
        
        logger.info(f"正在计算 {len(candidate_texts)} 篇论文的 embedding...")
        candidate_embs = self.model.encode(
            candidate_texts,
            batch_size=batch_size,
            normalize_embeddings=True,  # 归一化
            show_progress_bar=True,
            convert_to_tensor=False
        )
        
        # 计算相似度（归一化后，点积就是余弦相似度）
        logger.info("正在计算相似度分数...")
        
        # 转为 numpy 数组进行批量计算
        candidate_embs = np.array(candidate_embs)  # (n, 768)
        
        # 批量点积: (n, 768) @ (768,) = (n,)
        similarity_scores = candidate_embs @ source_emb
        
        # 组装结果
        scores = list(zip(candidate_papers, similarity_scores))
        
        # 按分数降序排序
        scores.sort(key=lambda x: x[1], reverse=True)
        
        logger.info(f"✅ 完成！分数范围: {scores[-1][1]:.3f} - {scores[0][1]:.3f}")
        
        return scores
    
    def filter_by_threshold(
        self,
        scored_papers: List[Tuple[Dict, float]],
        threshold: float = 0.5
    ) -> Tuple[List[Tuple[Dict, float]], List[Tuple[Dict, float]]]:
        """
        根据阈值分离高相关度和低相关度论文
        
        Args:
            scored_papers: 已评分的论文列表
            threshold: 相关度阈值
        
        Returns:
            (高相关度论文, 低相关度论文)
        """
        high_relevance = [(p, s) for p, s in scored_papers if s >= threshold]
        low_relevance = [(p, s) for p, s in scored_papers if s < threshold]
        
        logger.info(f"📊 相关度分级（阈值={threshold}）: 高相关度 {len(high_relevance)} 篇, 低相关度 {len(low_relevance)} 篇")
        
        return high_relevance, low_relevance
    
    def select_top_k(
        self,
        scored_papers: List[Tuple[Dict, float]],
        k: int = 15
    ) -> Tuple[List[Tuple[Dict, float]], List[Tuple[Dict, float]]]:
        """
        选择 top-k 高相关度论文
        
        Args:
            scored_papers: 已评分的论文列表
            k: 选择的论文数量
        
        Returns:
            (top-k 论文, 其他论文)
        """
        top_k = scored_papers[:k]
        others = scored_papers[k:]
        
        logger.info(f"📊 选择 Top-{k} 论文: 高相关度 {len(top_k)} 篇, 低相关度 {len(others)} 篇")
        
        if top_k:
            logger.info(f"分数范围: {top_k[-1][1]:.3f} - {top_k[0][1]:.3f}")
        
        return top_k, others
    
    def save_scores(
        self,
        scored_papers: List[Tuple[Dict, float]],
        output_path: Path
    ):
        """
        保存评分结果
        
        Args:
            scored_papers: 已评分的论文列表
            output_path: 输出文件路径
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        results = []
        for paper, score in scored_papers:
            results.append({
                'arxiv_id': paper.get('arxiv_id', paper.get('id', 'unknown')),
                'title': paper['title'],
                'score': float(score),
                'published': paper.get('published', ''),
                'authors': paper.get('authors', [])[:3]  # 只保存前3位作者
            })
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        logger.info(f"✅ 评分结果已保存: {output_path}")


# 测试代码
if __name__ == "__main__":
    # 示例数据
    source = {
        'title': 'Attention Is All You Need',
        'abstract': 'We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely.'
    }
    
    candidates = [
        {
            'arxiv_id': '1706.03762',
            'title': 'BERT: Pre-training of Deep Bidirectional Transformers',
            'abstract': 'We introduce a new language representation model called BERT, which stands for Bidirectional Encoder Representations from Transformers.',
            'authors': ['Jacob Devlin'],
            'published': '2018-10-11'
        },
        {
            'arxiv_id': '2005.14165',
            'title': 'GPT-3: Language Models are Few-Shot Learners',
            'abstract': 'Recent work has demonstrated substantial gains on many NLP tasks using pre-training.',
            'authors': ['Tom Brown'],
            'published': '2020-05-28'
        },
        {
            'arxiv_id': '1512.03385',
            'title': 'Deep Residual Learning for Image Recognition',
            'abstract': 'Deep neural networks are difficult to train. We present a residual learning framework.',
            'authors': ['Kaiming He'],
            'published': '2015-12-10'
        }
    ]
    
    print("=" * 70)
    print("相关度评分测试")
    print("=" * 70)
    
    scorer = RelevanceScorer()
    
    # 计算分数
    scored = scorer.score_papers(source, candidates)
    
    # 显示结果
    print("\n排序结果:")
    for i, (paper, score) in enumerate(scored, 1):
        print(f"{i}. [{score:.3f}] {paper['title'][:60]}...")
    
    # 选择 top-2
    top_k, others = scorer.select_top_k(scored, k=2)
    
    print("\nTop-2 高相关度论文:")
    for paper, score in top_k:
        print(f"  - [{score:.3f}] {paper['title']}")
