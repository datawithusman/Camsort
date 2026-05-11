import os
import time
from datetime import datetime, timezone

SORT_INTERVAL_SECONDS = int(os.getenv("SORT_INTERVAL_SECONDS", "30"))
GEMINI_MODE = os.getenv("GEMINI_MODE", "fake")
MAX_GEMINI_CALLS_PER_DAY = int(os.getenv("MAX_GEMINI_CALLS_PER_DAY", "100"))

gemini_calls_today = 0

def log(message: str):
    print(f"{datetime.now(timezone.utc).isoformat()} {message}", flush=True)

def run_once():
    global gemini_calls_today

    if GEMINI_MODE == "fake":
        log("worker_run status=success mode=fake gemini_calls=0")
        return

    if gemini_calls_today >= MAX_GEMINI_CALLS_PER_DAY:
        log("worker_run status=skipped reason=gemini_daily_limit")
        return

    gemini_calls_today += 1
    log(f"worker_run status=placeholder mode=real gemini_calls_today={gemini_calls_today}")

def main():
    log(f"GeminiCaller starting mode={GEMINI_MODE} interval_seconds={SORT_INTERVAL_SECONDS}")
    while True:
        run_once()
        time.sleep(SORT_INTERVAL_SECONDS)

if __name__ == "__main__":
    main()
