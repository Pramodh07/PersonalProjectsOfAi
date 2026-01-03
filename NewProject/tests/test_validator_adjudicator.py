from src.validator.rules import validate_entities
from src.adjudicator.engine import adjudicate_claim


def test_validator_and_adjudicator_flow():
    entities = [{"type": "patient", "value": "Jane"}, {"type": "amount", "value": "$15000"}]
    validation = validate_entities(entities)
    assert "results" in validation
    assert "signals" in validation
    decision = adjudicate_claim(entities, validation)
    assert decision.get("decision") in ("accept", "review", "reject")
