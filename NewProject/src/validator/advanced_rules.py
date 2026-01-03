# Add some rule helpers and a basic fraud check

def check_date_ranges(entities):
    # placeholder: ensure date fields are valid
    return []


def fraud_signals(entities):
    # simple heuristic: multiple identical claims or amounts > threshold
    signals = []
    for e in entities:
        if e.get("type") == "amount" and float(str(e.get("value", "0")).replace("$", "")) > 10000:
            signals.append({"signal": "large_amount", "amount": e.get("value")})
    return signals
