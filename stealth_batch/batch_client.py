import time, json
from typing import List, Optional
from pathlib import Path

from key_rotator.manager import KeyPoolManager
from stealth_config.config_manager import get_config

_BATCH_DIR = Path.home() / ".stealth" / "batch_jobs"
_FIREWORKS_BATCH_URL = "https://api.fireworks.ai/v1/batch"


class BatchInferenceClient:
    def __init__(self, pool=None, cfg=None):
        self.pool = pool or KeyPoolManager()
        self.cfg = cfg or get_config()
        self.enabled = self.cfg.is_enabled("batch")
        self.poll_interval = self.cfg.get("batch", "poll_interval_seconds", 30)
        self.max_batch_size = self.cfg.get("batch", "max_batch_size", 50)
        self.eligible_keywords = self.cfg.get("batch", "eligible_keywords", [])
        _BATCH_DIR.mkdir(parents=True, exist_ok=True)

    def is_eligible(self, task_hint: str) -> bool:
        if not self.enabled:
            return False
        hint_lower = task_hint.lower()
        return any(kw.lower() in hint_lower for kw in self.eligible_keywords)

    def submit_job(self, requests: List[dict], model: str) -> str:
        import httpx
        key = self.pool.get_active_key()
        job = {"model": model, "input_file": self._create_input_file(requests)}
        try:
            resp = httpx.post(_FIREWORKS_BATCH_URL, json=job, headers={"Authorization": f"Bearer {key}"}, timeout=30)
            if resp.status_code == 200:
                return resp.json().get("id", "")
            self.pool.report_failure(key)
            self.pool.rotate()
            return ""
        except Exception as e:
            self.pool.report_failure(key)
            self.pool.rotate()
            return ""

    def wait_for_completion(self, job_id: str) -> dict:
        if not job_id:
            return {"status": "failed", "reason": "no job_id"}
        import httpx
        key = self.pool.get_active_key()
        while True:
            try:
                resp = httpx.get(f"{_FIREWORKS_BATCH_URL}/{job_id}", headers={"Authorization": f"Bearer {key}"}, timeout=15)
                data = resp.json()
                status = data.get("status", "")
                if status in ("completed", "failed", "cancelled"):
                    return data
            except Exception:
                pass
            time.sleep(self.poll_interval)

    def submit_and_wait(self, requests: List[dict], model: str, timeout_seconds: int = 600) -> dict:
        job_id = self.submit_job(requests, model)
        if not job_id:
            return {"status": "failed", "reason": "submit_failed"}
        start = time.time()
        while time.time() - start < timeout_seconds:
            result = self.wait_for_completion(job_id)
            if result.get("status") != "in_progress":
                return result
        return {"status": "timeout", "job_id": job_id}

    def _create_input_file(self, requests: List[dict]) -> str:
        filepath = _BATCH_DIR / f"batch_{int(time.time())}.jsonl"
        lines = [json.dumps({"model": r.get("model", ""), "messages": r.get("messages", [])}) for r in requests]
        filepath.write_text("\n".join(lines))
        return str(filepath)


_batch_client = None


def get_batch_client() -> BatchInferenceClient:
    global _batch_client
    if _batch_client is None:
        _batch_client = BatchInferenceClient()
    return _batch_client


def batch_inference(requests: List[dict], model: str, wait: bool = True) -> dict:
    client = get_batch_client()
    if wait:
        return client.submit_and_wait(requests, model)
    job_id = client.submit_job(requests, model)
    return {"status": "submitted", "job_id": job_id}