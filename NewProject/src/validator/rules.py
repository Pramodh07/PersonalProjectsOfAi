# Simple rule-based validator

def validate_entities(entities):
    results = []
    for e in entities:
        if e.get("type") == "patient" and e.get("value"):
            results.append({"entity": e, "status": "pass", "confidence": 0.98})
        else:
            results.append({"entity": e, "status": "review", "confidence": 0.5})
    return results
