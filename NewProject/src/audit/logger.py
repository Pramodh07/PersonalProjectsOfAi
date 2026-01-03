import json
import time

# Minimal audit logger for PoC

def audit_event(claim_id, step, actor, payload):
    event = {
        "timestamp": time.time(),
        "claim_id": claim_id,
        "step": step,
        "actor": actor,
        "payload_summary": str(payload)[:1000]
    }
    # For PoC, write to a local file; replace with Postgres/ClickHouse for prod
    with open("audit.log", "a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")
    return event
