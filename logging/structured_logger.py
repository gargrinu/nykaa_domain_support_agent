import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

import json
import uuid
import time
from datetime import datetime
from guardrails.guardrails import mask_pii

LOG_FILE = "logs/request_logs.jsonl"

# Log Requests and Responses in ELK-style JSON Format:
def log_request(request_text: str, response_text: str):
    """
    Create one ELK-style JSON log entry.
    """
    start_time = time.time()
    masked_request = mask_pii(request_text)
    trace_id = str(uuid.uuid4())
    duration_ms = round((time.time() - start_time) * 1000, 2)
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "trace_id": trace_id,
        "request": masked_request,
        "response": response_text,
        "duration_ms": duration_ms
    }

    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(json.dumps(log_entry) + "\n")

    return trace_id