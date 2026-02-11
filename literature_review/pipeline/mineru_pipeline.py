import os
import time
import shutil
import zipfile
import requests
from pathlib import Path
from literature_review.logger import get_logger

logger = get_logger("mineru_pipeline")

# =================== 配置区 ===================
TOKEN = "eyJ0eXBlIjoiSldUIiwiYWxnIjoiSFM1MTIifQ.eyJqdGkiOiI0MDgwMDY0NSIsInJvbCI6IlJPTEVfUkVHSVNURVIiLCJpc3MiOiJPcGVuWExhYiIsImlhdCI6MTc3MDYxOTQxMiwiY2xpZW50SWQiOiJsa3pkeDU3bnZ5MjJqa3BxOXgydyIsInBob25lIjoiIiwib3BlbklkIjpudWxsLCJ1dWlkIjoiNGIwYmRmZTEtNDcxMS00ZjBhLTgzN2YtZTQyNjFmM2U1NDI1IiwiZW1haWwiOiIiLCJleHAiOjE3NzE4MjkwMTJ9.onFsgudPG71DzQGzo0tJKhqOiRH4ZI7o1DSL0_W519ONDC_UNaT4sSQBXyDZmp-jpWVo1UbhdbYkikly9vTtlg"

FILE = Path("../input/2401.12345.pdf")           # 本地PDF
MODEL_VERSION = "vlm"

POLL_INTERVAL = 5
POLL_TIMEOUT = 300

PROJECT_ROOT = Path(".")                      # 在 literature_review 目录运行就用 "."
OUT_BASE = PROJECT_ROOT / "outputs"           # 输出根目录
PAPER_ID = FILE.stem                          # 默认用文件名（2401.12345）
KEEP_ZIP = True
KEEP_META = True
# =============================================


def apply_upload_url(token: str, file_path: Path, model_version: str) -> tuple[str, str]:
    """申请上传URL，返回 (batch_id, upload_url)"""
    apply_url = "https://mineru.net/api/v4/file-urls/batch"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {
        "files": [{"name": file_path.name, "data_id": file_path.stem}],
        "model_version": model_version,
    }
    r = requests.post(apply_url, headers=headers, json=payload, timeout=30)
    r.raise_for_status()
    j = r.json()
    if j.get("code") != 0:
        raise RuntimeError(f"申请上传URL失败: {j}")
    logger.debug(f"apply: {j}")
    return j["data"]["batch_id"], j["data"]["file_urls"][0]


def put_upload_file(file_path: Path, upload_url: str) -> None:
    """PUT 上传本地文件到预签名URL"""
    with open(file_path, "rb") as f:
        u = requests.put(upload_url, data=f, timeout=300)
    u.raise_for_status()


def get_batch_result_once(token: str, batch_id: str) -> dict:
    """查询一次 batch 结果"""
    url = f"https://mineru.net/api/v4/extract-results/batch/{batch_id}"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    res = requests.get(url, headers=headers, timeout=30)
    res.raise_for_status()
    j = res.json()
    if j.get("code") != 0:
        raise RuntimeError(f"查询结果失败: {j}")
    return j


def poll_until_done(token: str, batch_id: str, timeout: int, interval: int) -> dict:
    """轮询直到 done，返回最终 json"""
    start = time.time()
    while True:
        j = get_batch_result_once(token, batch_id)
        data = j.get("data", {})
        items = data.get("extract_result") or []

        if items:
            item0 = items[0]
            state = (item0.get("state") or "").lower()
            zip_url = item0.get("full_zip_url")
            logger.info(f"[{batch_id}] state={state}")

            if state == "done" and zip_url:
                return j

        if time.time() - start > timeout:
            raise TimeoutError(f"等待超时（>{timeout}s），最后一次返回：{j}")

        time.sleep(interval)


def download_file(url: str, out_path: Path, timeout: int = 300) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with requests.get(url, stream=True, timeout=timeout) as r:
        r.raise_for_status()
        with open(out_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)


def safe_extract_zip(zip_path: Path, extract_dir: Path) -> None:
    extract_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as z:
        # 防 zip slip
        for member in z.infolist():
            target = (extract_dir / member.filename).resolve()
            if not str(target).startswith(str(extract_dir.resolve())):
                raise RuntimeError(f"Unsafe zip path detected: {member.filename}")
        z.extractall(extract_dir)


def persist_result(zip_url: str, out_dir: Path, keep_zip: bool, keep_meta: bool) -> None:
    """
    下载zip->解压->把 full.md + images 持久化到 out_dir
    """
    out_dir.mkdir(parents=True, exist_ok=True)

    zip_path = out_dir / "mineru_result.zip"
    tmp_dir = out_dir / "_tmp_extract"

    # 下载
    download_file(zip_url, zip_path)

    # 解压
    if tmp_dir.exists():
        shutil.rmtree(tmp_dir)
    safe_extract_zip(zip_path, tmp_dir)

    # 找到 full.md 所在目录（通常有一层UUID目录）
    full_mds = list(tmp_dir.rglob("full.md"))
    if not full_mds:
        raise FileNotFoundError("解压后未找到 full.md（zip结构可能变化）")
    full_md_src = full_mds[0]
    base_dir = full_md_src.parent

    # 拷贝 full.md
    shutil.copy2(full_md_src, out_dir / "full.md")

    # 拷贝 images/
    images_src = base_dir / "images"
    images_dst = out_dir / "images"
    if images_src.exists():
        if images_dst.exists():
            shutil.rmtree(images_dst)
        shutil.copytree(images_src, images_dst)
    else:
        logger.warning("未发现 images 目录（可能该文档无图片或输出结构变了）")

    # 保存其他文件到 meta/
    if keep_meta:
        meta_dir = out_dir / "meta"
        meta_dir.mkdir(exist_ok=True)
        for p in base_dir.iterdir():
            if p.name in {"images", "full.md"}:
                continue
            dst = meta_dir / p.name
            if p.is_dir():
                if dst.exists():
                    shutil.rmtree(dst)
                shutil.copytree(p, dst)
            else:
                shutil.copy2(p, dst)

    # 清理临时
    shutil.rmtree(tmp_dir)
    if not keep_zip:
        zip_path.unlink(missing_ok=True)


def main():
    if not TOKEN:
        raise RuntimeError("未设置 MINERU_TOKEN。请先：export MINERU_TOKEN='你的token'")
    if not FILE.exists():
        raise FileNotFoundError(f"找不到文件：{FILE.resolve()}")

    # 1) 申请上传URL
    batch_id, upload_url = apply_upload_url(TOKEN, FILE, MODEL_VERSION)

    # 2) 上传
    put_upload_file(FILE, upload_url)
    logger.info(f"upload ok, batch_id = {batch_id}")

    # 3) 轮询拿结果
    final_json = poll_until_done(TOKEN, batch_id, timeout=POLL_TIMEOUT, interval=POLL_INTERVAL)
    item0 = final_json["data"]["extract_result"][0]
    zip_url = item0["full_zip_url"]
    data_id = item0.get("data_id") or PAPER_ID

    logger.info(f"✅ done. full_zip_url = {zip_url}")

    # 4) 持久化保存 full.md + images
    out_dir = OUT_BASE / str(data_id)
    persist_result(zip_url, out_dir, keep_zip=KEEP_ZIP, keep_meta=KEEP_META)

    logger.info(f"✅ 已保存到： {out_dir.resolve()}")
    logger.info(f"   - full.md: {(out_dir / 'full.md').resolve()}")
    logger.info(f"   - images/: {(out_dir / 'images').resolve()}")


if __name__ == "__main__":
    main()
