from __future__ import annotations
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; BASE=ROOT/"backend"/"artifacts"/"battery"/"production"; schema=json.loads((BASE/"feature_schema.json").read_text())
try: import torch
except ImportError: torch=None
for path in sorted(BASE.rglob("*")):
    if not path.is_file(): continue
    row={"path":str(path.relative_to(ROOT)),"type":path.suffix,"bytes":path.stat().st_size,"sha256":hashlib.sha256(path.read_bytes()).hexdigest()}
    if path.suffix==".pt" and torch:
        model=torch.jit.load(str(path),map_location="cpu"); row["graph_signature"]=str(model.forward.schema); row["expected_output_shape"]="[batch]"
    print(json.dumps(row))
print(json.dumps({"feature_count":schema["feature_count"],"feature_names":schema["feature_names"],"preprocessing":"SimpleImputer(median) then StandardScaler"}))
