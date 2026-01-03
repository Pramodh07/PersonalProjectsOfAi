# Basic policy engine rules for adjudication

def apply_policy(entities, validation):
    # Very simple policy: if any validation result is 'fail', return reject
    for v in validation.get("results", []):
        if v.get("status") == "fail":
            return {"decision": "reject", "reason": "validation_failed"}
    # interpret fraud signals
    if validation.get("signals"):
        return {"decision": "review", "reason": "fraud_signals"}
    return {"decision": "accept", "payout": 100.0}