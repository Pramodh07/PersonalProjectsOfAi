# Simple rule-based validator with pluggable advanced checks
from .advanced_rules import fraud_signals


def validate_entities(entities):
    results = []
    for e in entities:
        if e.get("type") == "patient" and e.get("value"):
            results.append({"entity": e, "status": "pass", "confidence": 0.98})
        else:
            results.append({"entity": e, "status": "review", "confidence": 0.5})

    # add fraud signals metadata
    signals = fraud_signals(entities)
    return {"results": results, "signals": signals}

