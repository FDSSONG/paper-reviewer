"""
一键式端到端流水线 — 从 PDF 到评审报告

直接串联现有 4 个 pipeline：
  Stage 1: mineru_pipeline          → PDF → Markdown
  Stage 2: literature_search_pipeline → 元数据 → 查询 → arXiv 检索
  Stage 3: ranking_and_summary_pipeline → 评分 → Top-K → 摘要
  Stage 4: review_pipeline          → 评审报告生成

用法：
  python full_pipeline.py 2401.12345.pdf
  python full_pipeline.py 2401.12345.pdf --skip-mineru
  python full_pipeline.py 2401.12345.pdf --stage 3
"""

import sys
import time
import argparse
import logging
from pathlib import Path

# 确保 import 路径正确
PIPELINE_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(PIPELINE_DIR.parent.parent))

# 复用现有 pipeline
from literature_review.pipeline.mineru_pipeline import (
    main as mineru_main,
    apply_upload_url, put_upload_file, poll_until_done, persist_result,
    TOKEN as DEFAULT_TOKEN,
)
from literature_review.pipeline.literature_search_pipeline import run_literature_search
from literature_review.pipeline.ranking_and_summary_pipeline import run_ranking_and_summary
from literature_review.pipeline.review_pipeline import run_review_generation
from literature_review.logger import setup_logger, get_logger

logger = get_logger("full_pipeline")


def run_stage1(pdf_path: Path, paper_id: str, outputs_dir: Path,
               token: str = None, model_version: str = "vlm"):
    """
    Stage 1: PDF → Markdown (MinerU)

    mineru_pipeline.main() 使用硬编码的全局变量，不方便传参，
    因此这里直接调用它内部的函数来组装流程。
    """
    out_dir = outputs_dir / paper_id
    full_md = out_dir / "full.md"

    if full_md.exists():
        logger.info("⏭️  full.md 已存在，跳过 MinerU 解析")
        return full_md

    tk = token or DEFAULT_TOKEN

    logger.info("📤 上传 PDF 到 MinerU...")
    batch_id, upload_url = apply_upload_url(tk, pdf_path, model_version)
    put_upload_file(pdf_path, upload_url)
    logger.info(f"✅ 上传完成, batch_id = {batch_id}")

    logger.info("⏳ 等待 MinerU 解析...")
    final_json = poll_until_done(tk, batch_id, timeout=300, interval=5)
    zip_url = final_json["data"]["extract_result"][0]["full_zip_url"]

    logger.info("📥 下载并解压结果...")
    persist_result(zip_url, out_dir, keep_zip=True, keep_meta=True)
    logger.info(f"✅ 已保存: {full_md}")
    return full_md


def run_full_pipeline(
    pdf_path: str,
    start_stage: int = 1,
    num_queries: int = 7,
    since_year: int = 2020,
    max_results_per_query: int = 20,
    top_k: int = 15,
    language: str = "chinese",
    skip_mineru: bool = False,
    mineru_token: str = None,
):
    """一键运行完整流水线"""
    pdf_path = Path(pdf_path).resolve()
    paper_id = pdf_path.stem
    outputs_dir = PIPELINE_DIR / "outputs"
    results_dir = PIPELINE_DIR / "literature_search_results"

    total_start = time.time()

    logger.info("╔" + "═" * 68 + "╗")
    logger.info("║" + "  🚀 学术论文一键评审流水线".center(58) + "║")
    logger.info("╚" + "═" * 68 + "╝")
    logger.info(f"PDF: {pdf_path} | 论文 ID: {paper_id} | 起始阶段: Stage {start_stage} | 语言: {language} | Top-K: {top_k}")
    logger.info("─" * 70)

    # ──── Stage 1: PDF → Markdown ────
    if start_stage <= 1:
        logger.info("\n▶ Stage 1/4: PDF → Markdown (MinerU)")
        logger.info("─" * 70)
        if skip_mineru:
            full_md = outputs_dir / paper_id / "full.md"
            if not full_md.exists():
                logger.error(f"--skip-mineru 但 {full_md} 不存在")
                sys.exit(1)
            logger.info("⏭️  跳过 MinerU（已有 full.md）")
        else:
            if not pdf_path.exists():
                logger.error(f"PDF 不存在: {pdf_path}")
                sys.exit(1)
            run_stage1(pdf_path, paper_id, outputs_dir, token=mineru_token)

    # ──── Stage 2: 文献检索 ────
    if start_stage <= 2:
        logger.info("\n▶ Stage 2/4: 元数据提取 → 查询生成 → arXiv 检索")
        logger.info("─" * 70)
        run_literature_search(
            paper_id=paper_id,
            num_queries=num_queries,
            since_year=since_year,
            max_results_per_query=max_results_per_query,
            output_dir=str(results_dir),
        )

    # ──── Stage 3: 评分 + 摘要 ────
    if start_stage <= 3:
        logger.info("\n▶ Stage 3/4: 相关度评分 → Top-K 筛选 → 摘要生成")
        logger.info("─" * 70)
        run_ranking_and_summary(
            paper_id=paper_id,
            top_k=top_k,
            language=language,
            input_dir=str(results_dir),
        )

    # ──── Stage 4: 评审报告 ────
    if start_stage <= 4:
        logger.info("\n▶ Stage 4/4: 生成结构化评审报告")
        logger.info("─" * 70)
        run_review_generation(
            paper_id=paper_id,
            language=language,
            input_dir=str(results_dir),
        )

    # ──── 汇总 ────
    elapsed = time.time() - total_start
    m, s = int(elapsed // 60), int(elapsed % 60)

    logger.info("═" * 70)
    logger.info(f"✅ 全部完成！总耗时 {m}分{s}秒")
    logger.info(f"📝 评审报告: {results_dir / paper_id / f'review_report_{language}.md'}")
    logger.info("═" * 70)


def main():
    parser = argparse.ArgumentParser(
        description='学术论文一键评审 — 从 PDF 到评审报告',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python full_pipeline.py ../../2401.12345.pdf                    # 完整流程
  python full_pipeline.py ../../2401.12345.pdf --skip-mineru      # 跳过 PDF 解析
  python full_pipeline.py ../../2401.12345.pdf --stage 3          # 从 Stage 3 续跑
  python full_pipeline.py ../../2401.12345.pdf -k 10 -l english   # 自定义参数
"""
    )

    parser.add_argument('pdf_path', help='PDF 文件路径')
    parser.add_argument('--stage', type=int, default=1, choices=[1, 2, 3, 4],
                        help='从第几阶段开始（默认: 1）')
    parser.add_argument('-n', '--num-queries', type=int, default=7,
                        help='检索查询数量（默认: 7）')
    parser.add_argument('-y', '--since-year', type=int, default=2020,
                        help='起始年份（默认: 2020）')
    parser.add_argument('-r', '--max-results', type=int, default=20,
                        help='每条查询最大结果数（默认: 20）')
    parser.add_argument('-k', '--top-k', type=int, default=15,
                        help='高相关度论文数量（默认: 15）')
    parser.add_argument('-l', '--language', choices=['chinese', 'english'],
                        default='chinese', help='输出语言（默认: chinese）')
    parser.add_argument('--skip-mineru', action='store_true',
                        help='跳过 MinerU 解析（已有 full.md）')
    parser.add_argument('--mineru-token', default=None,
                        help='MinerU API Token')

    args = parser.parse_args()

    # 初始化日志系统
    outputs_dir = PIPELINE_DIR / "outputs"
    log_dir = outputs_dir / "logs"
    setup_logger(name="literature_review", log_dir=log_dir, level=logging.INFO)

    try:
        run_full_pipeline(
            pdf_path=args.pdf_path,
            start_stage=args.stage,
            num_queries=args.num_queries,
            since_year=args.since_year,
            max_results_per_query=args.max_results,
            top_k=args.top_k,
            language=args.language,
            skip_mineru=args.skip_mineru,
            mineru_token=args.mineru_token,
        )
    except KeyboardInterrupt:
        logger.warning("用户中断")
        sys.exit(130)
    except Exception as e:
        logger.exception(f"失败: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
