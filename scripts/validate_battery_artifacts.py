from __future__ import annotations
import json,math
from pathlib import Path
import joblib,numpy as np
ROOT=Path(__file__).resolve().parents[1]; BASE=ROOT/"backend"/"artifacts"/"battery"/"production"
try: import torch
except ImportError: raise SystemExit("BLOCKED: PyTorch is not installed; install backend requirements")
schema=json.loads((BASE/"feature_schema.json").read_text()); assert schema["feature_count"]==len(schema["feature_names"])==24
imp=joblib.load(BASE/"feature_imputer.joblib"); scale=joblib.load(BASE/"feature_scaler.joblib"); raw=np.tile(np.asarray(imp.statistics_,dtype=float),(2,1)); x=torch.tensor(scale.transform(imp.transform(raw)),dtype=torch.float32); cycle=torch.tensor([1.,100.])
outputs=[]
for seed in (13,42,77):
    model=torch.jit.load(str(BASE/"physics_regularized_mlp"/f"model_seed_{seed}_torchscript.pt"),map_location="cpu").eval(); one=model(x,cycle).detach().numpy(); two=model(x,cycle).detach().numpy(); assert one.shape==(2,) and np.isfinite(one).all() and np.array_equal(one,two); outputs.append(one)
ensemble=np.vstack(outputs); assert np.isfinite(ensemble.mean()) and ensemble.std()>=0 and (ensemble>.4).all() and (ensemble<1.2).all()
emp=json.loads((BASE/"empirical_parameters.json").read_text()); reference=emp["c"]-emp["a_sqrt_cycle"]*math.sqrt(100)-emp["b_cycle"]*100; assert math.isfinite(reference)
rec=json.loads((BASE/"deployment_recommendation.json").read_text()); assert rec["benchmark_selected_model"]=="Physics-regularized MLP"
print(json.dumps({"status":"PASS","device":"cpu","cuda_required":False,"feature_count":24,"signature":str(model.forward.schema),"outputs":ensemble.tolist(),"ensemble_mean":ensemble.mean(axis=0).tolist(),"ensemble_dispersion":ensemble.std(axis=0).tolist(),"empirical_cycle_100":reference},indent=2))
