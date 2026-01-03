# Simple adjudication engine for PoC
from .policy import apply_policy


def adjudicate_claim(entities, validation_results):
    # validation_results is expected to be a dict with results and signals
    return apply_policy(entities, validation_results)

