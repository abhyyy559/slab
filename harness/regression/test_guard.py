"""Guard suite: must pass on every version bump before strategy changes are committed."""
import json, pathlib

def test_command_schema():
    p = pathlib.Path("commands/phone_delivery_check.json")
    assert p.exists(), "Command JSON file must exist"
    data = json.loads(p.read_text(encoding="utf-8"))
    for key in ["workflow", "version", "template", "params", "preconditions", "negative_case"]:
        assert key in data, f"Missing required key: {key}"

def test_template_integrity():
    p = pathlib.Path("commands/phone_delivery_check.json")
    data = json.loads(p.read_text(encoding="utf-8"))
    template = data["template"]
    assert len(template) >= 4, "Template must have at least 4 steps"
    for step in template:
        assert "step" in step and "intent" in step and "target" in step
        assert isinstance(step["target"], dict)

def test_params_present():
    p = pathlib.Path("commands/phone_delivery_check.json")
    data = json.loads(p.read_text(encoding="utf-8"))
    params = data.get("params", {})
    assert "budget" in params and "ram" in params and "pin" in params

