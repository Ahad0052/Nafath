"""Prefect server healthcheck with debug logging."""
import json
import sys
import time
import urllib.error
import urllib.request

LOG_PATH = "/debug/debug-72a1c8.log"
URL = "http://localhost:4200/api/health"


def _log(hypothesis_id, message, data):
    # #region agent log
    entry = {
        "sessionId": "72a1c8",
        "hypothesisId": hypothesis_id,
        "location": "debug_healthcheck.py",
        "message": message,
        "data": data,
        "timestamp": int(time.time() * 1000),
    }
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass
    # #endregion


def main():
    start = time.time()
    try:
        with urllib.request.urlopen(URL, timeout=4) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            elapsed_ms = int((time.time() - start) * 1000)
            _log(
                "H1",
                "healthcheck_success",
                {"status": resp.status, "elapsed_ms": elapsed_ms, "body": body[:200]},
            )
            sys.exit(0)
    except urllib.error.URLError as exc:
        elapsed_ms = int((time.time() - start) * 1000)
        _log(
            "H2",
            "healthcheck_failed",
            {"error": str(exc.reason), "elapsed_ms": elapsed_ms},
        )
        sys.exit(1)
    except Exception as exc:
        elapsed_ms = int((time.time() - start) * 1000)
        _log(
            "H2",
            "healthcheck_exception",
            {"error": str(exc), "elapsed_ms": elapsed_ms},
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
