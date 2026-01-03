# Simple adjudication engine for PoC

def adjudicate_claim(entities, validation_results):
    # Very simple logic: if any validation is 'fail' -> reject
    for v in validation_results:
        if v.get("status") == "fail":
            return {"decision": "reject", "reason": "validation_failed"}
    # otherwise accept and return estimated payout (mock)
    return {"decision": "accept", "payout": 100.0}
