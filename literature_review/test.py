import requests
from pathlib import Path
import time

# ====== 配置 ======
token = "eyJ0eXBlIjoiSldUIiwiYWxnIjoiSFM1MTIifQ.eyJqdGkiOiI0MDgwMDY0NSIsInJvbCI6IlJPTEVfUkVHSVNURVIiLCJpc3MiOiJPcGVuWExhYiIsImlhdCI6MTc3MDYxOTQxMiwiY2xpZW50SWQiOiJsa3pkeDU3bnZ5MjJqa3BxOXgydyIsInBob25lIjoiIiwib3BlbklkIjpudWxsLCJ1dWlkIjoiNGIwYmRmZTEtNDcxMS00ZjBhLTgzN2YtZTQyNjFmM2U1NDI1IiwiZW1haWwiOiIiLCJleHAiOjE3NzE4MjkwMTJ9.onFsgudPG71DzQGzo0tJKhqOiRH4ZI7o1DSL0_W519ONDC_UNaT4sSQBXyDZmp-jpWVo1UbhdbYkikly9vTtlg"
FILE = Path("input/2401.12345.pdf")
MODEL_VERSION = "vlm"

POLL_INTERVAL = 5   # 每隔多少秒查一次
POLL_TIMEOUT = 300  # 最多等待多少秒
# ===================


def upload_local_pdf_get_batch_id(token: str, file_path: Path, model_version: str) -> str:
    """申请上传URL + PUT上传，返回 batch_id"""
    apply_url = "https://mineru.net/api/v4/file-urls/batch"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {
        "files": [{"name": file_path.name, "data_id": file_path.stem}],
        "model_version": model_version
    }

    r = requests.post(apply_url, headers=headers, json=payload, timeout=30)
    r.raise_for_status()
    j = r.json()
    print("apply:", j)

    batch_id = j["data"]["batch_id"]
    upload_url = j["data"]["file_urls"][0]

    with open(file_path, "rb") as f:
        u = requests.put(upload_url, data=f, timeout=300)
    u.raise_for_status()

    print("upload ok, batch_id =", batch_id)
    return batch_id


def get_batch_result_once(token: str, batch_id: str) -> dict:
    """查询一次 batch 结果"""
    url = f"https://mineru.net/api/v4/extract-results/batch/{batch_id}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    res = requests.get(url, headers=headers, timeout=30)
    res.raise_for_status()
    j = res.json()
    return j


def poll_batch_result(token: str, batch_id: str, timeout: int, interval: int) -> dict:
    start = time.time()

    while True:
        j = get_batch_result_once(token, batch_id)
        data = j.get("data", {})

        # 你的接口返回：结果在 data["extract_result"] 列表里
        items = data.get("extract_result") or []
        if items:
            # 你只传了一个文件，通常取第 0 个
            item0 = items[0]
            state = (item0.get("state") or "").lower()
            zip_url = item0.get("full_zip_url")

            print(f"[{batch_id}] state={state}")

            # done 就返回（或者 zip_url 有值也算完成）
            if state == "done" or zip_url:
                return j

        # 超时判断
        if time.time() - start > timeout:
            raise TimeoutError(f"等待超时（>{timeout}s），最后一次返回：{j}")

        time.sleep(interval)


if __name__ == "__main__":
    if not FILE.exists():
        raise FileNotFoundError(f"找不到文件：{FILE.resolve()}")

    batch_id = upload_local_pdf_get_batch_id(token, FILE, MODEL_VERSION)

    # 查询结果（轮询）
    final_json = poll_batch_result(token, batch_id, timeout=POLL_TIMEOUT, interval=POLL_INTERVAL)

    print("status_code: 200")  # requests.raise_for_status 已确保是 2xx
    print(final_json)
    print(final_json["data"])
