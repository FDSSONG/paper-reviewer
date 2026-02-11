#!/usr/bin/env python3
"""
PDF 处理模块
批量下载和转换高相关度论文的 PDF
"""
import os
import time
import requests
import shutil
from pathlib import Path
from typing import List, Dict, Optional
from literature_review.logger import get_logger

logger = get_logger("pdf_processor")


class PDFProcessor:
    """PDF 处理器"""
    
    def __init__(self, mineru_token: Optional[str] = None):
        """
        初始化处理器
        
        Args:
            mineru_token: MinerU API token
        """
        self.mineru_token = mineru_token or os.getenv('MINERU_TOKEN')
        if not self.mineru_token:
            logger.warning("未设置 MINERU_TOKEN，PDF 转换功能将不可用")
    
    def download_pdf(
        self,
        arxiv_id: str,
        output_dir: Path,
        timeout: int = 60,
        max_retries: int = 3
    ) -> Optional[Path]:
        """
        从 arXiv 下载 PDF（带指数退避重试）
        
        Args:
            arxiv_id: arXiv ID (例如 '2301.12345')
            output_dir: 输出目录
            timeout: 下载超时时间（秒）
            max_retries: 最大重试次数
        
        Returns:
            下载的 PDF 文件路径，失败返回 None
        """
        # 构建 PDF URL
        pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
        
        output_dir.mkdir(parents=True, exist_ok=True)
        pdf_path = output_dir / f"{arxiv_id}.pdf"
        
        # 如果已存在，跳过下载
        if pdf_path.exists() and pdf_path.stat().st_size > 1000:
            logger.info(f"PDF 已存在: {arxiv_id}")
            return pdf_path
        
        last_error = None
        for attempt in range(max_retries + 1):
            try:
                logger.info(f"📥 下载 PDF: {arxiv_id}")
                response = requests.get(pdf_url, timeout=timeout, stream=True)
                response.raise_for_status()
                
                with open(pdf_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                # 验证文件完整性（PDF 至少应该有几 KB）
                if pdf_path.stat().st_size < 1000:
                    raise IOError(f"下载的文件过小 ({pdf_path.stat().st_size} bytes)，可能不完整")
                
                logger.info(f"✅ 下载完成: {pdf_path}")
                return pdf_path
            
            except Exception as e:
                last_error = e
                # 清理不完整文件
                if pdf_path.exists():
                    pdf_path.unlink()
                
                error_str = str(e)
                retryable = any(keyword in error_str for keyword in [
                    'IncompleteRead', 'Connection', 'RemoteDisconnected',
                    'ConnectionReset', 'Timeout', 'timeout',
                    'Connection broken', 'Connection aborted'
                ])
                
                if retryable and attempt < max_retries:
                    wait = 3 * (2 ** attempt)  # 指数退避: 3s, 6s, 12s
                    logger.warning(f"下载失败: {e}")
                    logger.info(f"第 {attempt + 1} 次重试，等待 {wait}s...")
                    time.sleep(wait)
                else:
                    logger.error(f"下载失败: {e}")
                    return None
        
        logger.error(f"下载失败（已重试 {max_retries} 次）: {last_error}")
        return None
    
    def convert_pdf_to_markdown(
        self,
        pdf_path: Path,
        output_dir: Path,
        model_version: str = "vlm"
    ) -> Optional[Path]:
        """
        使用 MinerU API 将 PDF 转换为 Markdown
        
        Args:
            pdf_path: PDF 文件路径
            output_dir: 输出目录
            model_version: 模型版本
        
        Returns:
            生成的 Markdown 文件路径，失败返回 None
        """
        if not self.mineru_token:
            logger.warning("未设置 MINERU_TOKEN，跳过转换")
            return None
        
        # 检查是否已存在
        md_path = output_dir / "full.md"
        if md_path.exists():
            logger.info(f"Markdown 已存在: {md_path}")
            return md_path
        
        try:
            logger.info(f"🔄 转换 PDF 为 Markdown: {pdf_path.name}")
            
            # 1) 申请上传 URL
            batch_id, upload_url = self._apply_upload_url(pdf_path, model_version)
            
            # 2) 上传文件
            self._upload_file(pdf_path, upload_url)
            logger.info(f"✅ 上传完成, batch_id = {batch_id}")
            
            # 3) 轮询结果
            result = self._poll_result(batch_id, timeout=300, interval=5)
            
            # 4) 下载并保存
            zip_url = result['data']['extract_result'][0]['full_zip_url']
            self._download_and_extract(zip_url, output_dir)
            
            logger.info(f"✅ 转换完成: {md_path}")
            return md_path
        
        except Exception as e:
            logger.error(f"转换失败: {e}")
            return None
    
    def _apply_upload_url(self, pdf_path: Path, model_version: str):
        """申请上传 URL"""
        url = "https://mineru.net/api/v4/file-urls/batch"
        headers = {
            "Authorization": f"Bearer {self.mineru_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "files": [{"name": pdf_path.name, "data_id": pdf_path.stem}],
            "model_version": model_version
        }
        
        r = requests.post(url, headers=headers, json=payload, timeout=30)
        r.raise_for_status()
        j = r.json()
        
        if j.get("code") != 0:
            raise RuntimeError(f"申请上传URL失败: {j}")
        
        return j["data"]["batch_id"], j["data"]["file_urls"][0]
    
    def _upload_file(self, pdf_path: Path, upload_url: str):
        """上传文件"""
        with open(pdf_path, "rb") as f:
            r = requests.put(upload_url, data=f, timeout=300)
        r.raise_for_status()
    
    def _poll_result(self, batch_id: str, timeout: int, interval: int):
        """轮询结果"""
        url = f"https://mineru.net/api/v4/extract-results/batch/{batch_id}"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.mineru_token}"
        }
        
        start = time.time()
        while True:
            r = requests.get(url, headers=headers, timeout=30)
            r.raise_for_status()
            j = r.json()
            
            if j.get("code") != 0:
                raise RuntimeError(f"查询结果失败: {j}")
            
            items = j.get("data", {}).get("extract_result", [])
            if items:
                state = items[0].get("state", "").lower()
                if state == "done" and items[0].get("full_zip_url"):
                    return j
            
            if time.time() - start > timeout:
                raise TimeoutError(f"等待超时（>{timeout}s）")
            
            time.sleep(interval)
    
    def _download_and_extract(self, zip_url: str, output_dir: Path):
        """下载并解压结果"""
        import zipfile
        
        output_dir.mkdir(parents=True, exist_ok=True)
        zip_path = output_dir / "result.zip"
        tmp_dir = output_dir / "_tmp"
        
        # 下载
        with requests.get(zip_url, stream=True, timeout=300) as r:
            r.raise_for_status()
            with open(zip_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024*1024):
                    f.write(chunk)
        
        # 解压
        if tmp_dir.exists():
            shutil.rmtree(tmp_dir)
        
        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(tmp_dir)
        
        # 找到 full.md
        full_mds = list(tmp_dir.rglob("full.md"))
        if not full_mds:
            raise FileNotFoundError("未找到 full.md")
        
        full_md_src = full_mds[0]
        base_dir = full_md_src.parent
        
        # 拷贝文件
        shutil.copy2(full_md_src, output_dir / "full.md")
        
        images_src = base_dir / "images"
        images_dst = output_dir / "images"
        if images_src.exists():
            if images_dst.exists():
                shutil.rmtree(images_dst)
            shutil.copytree(images_src, images_dst)
        
        # 清理
        shutil.rmtree(tmp_dir)
        zip_path.unlink()
    
    def batch_process(
        self,
        papers: List[Dict],
        output_base_dir: Path,
        download_only: bool = False
    ) -> List[Dict]:
        """
        批量处理论文
        
        Args:
            papers: 论文列表
            output_base_dir: 输出根目录
            download_only: 是否只下载不转换
        
        Returns:
            处理结果列表
        """
        results = []
        
        for i, paper in enumerate(papers, 1):
            arxiv_id = paper.get('arxiv_id', paper.get('id', ''))
            title = paper.get('title', '')[:60]
            
            logger.info(f"[{i}/{len(papers)}] 处理: {arxiv_id} - {title}...")
            
            paper_dir = output_base_dir / arxiv_id
            
            # 下载 PDF
            pdf_path = self.download_pdf(arxiv_id, paper_dir)
            
            if not pdf_path:
                results.append({
                    'arxiv_id': arxiv_id,
                    'status': 'download_failed',
                    'pdf_path': None,
                    'md_path': None
                })
                continue
            
            # 转换为 Markdown
            if download_only:
                md_path = None
            else:
                md_path = self.convert_pdf_to_markdown(pdf_path, paper_dir)
            
            results.append({
                'arxiv_id': arxiv_id,
                'status': 'success' if md_path or download_only else 'conversion_failed',
                'pdf_path': str(pdf_path),
                'md_path': str(md_path) if md_path else None
            })
            
            # 避免触发速率限制
            if i < len(papers):
                time.sleep(2)
        
        return results


# 测试代码
if __name__ == "__main__":
    processor = PDFProcessor()
    
    # 测试下载
    test_dir = Path("test_pdfs")
    pdf_path = processor.download_pdf("2301.12345", test_dir)
    
    if pdf_path:
        logger.info(f"✅ 测试成功: {pdf_path}")
