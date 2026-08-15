import json,math
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]/"artifacts"/"battery"/"production"
def test_schema_and_empirical():
    schema=json.loads((BASE/"feature_schema.json").read_text()); assert schema["feature_count"]==len(schema["feature_names"])==24
    p=json.loads((BASE/"empirical_parameters.json").read_text()); assert math.isfinite(p["c"]-p["a_sqrt_cycle"]*10-p["b_cycle"]*100)
