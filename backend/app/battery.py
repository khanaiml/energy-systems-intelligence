from __future__ import annotations

import math
from functools import lru_cache

import joblib
import numpy as np
import torch
from pydantic import BaseModel, ConfigDict, Field, model_validator

from .core import ARTIFACTS, read_json

BASE = ARTIFACTS / "battery" / "production"


class BatteryEstimateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    cycle_index: float = Field(ge=0, le=10000)
    features: dict[str, float | None]
    case_id: str | None = Field(default=None, max_length=100)

    @model_validator(mode="after")
    def validate_features(self):
        names = set(read_json(BASE / "feature_schema.json")["feature_names"])
        unknown = set(self.features) - names
        if unknown:
            raise ValueError(f"unexpected features: {sorted(unknown)}")
        missing = names - set(self.features)
        if len(missing) > 8:
            raise ValueError("more than 8 features are missing")
        if not self.features:
            raise ValueError("empty feature object")
        return self


@lru_cache
def load_bundle():
    schema = read_json(BASE / "feature_schema.json")
    models = [
        torch.jit.load(str(BASE / "physics_regularized_mlp" / f"model_seed_{seed}_torchscript.pt"), map_location="cpu").eval()
        for seed in (13, 42, 77)
    ]
    return schema, joblib.load(BASE / "feature_imputer.joblib"), joblib.load(BASE / "feature_scaler.joblib"), models


def estimate(req: BatteryEstimateRequest):
    schema, imputer, scaler, models = load_bundle()
    names = schema["feature_names"]
    values = dict(req.features)
    # Cycle-derived fields are explicit benchmark inputs; keep them consistent with cycle_index.
    values.setdefault("cycle_index", req.cycle_index)
    values.setdefault("cycle_sqrt", math.sqrt(req.cycle_index))
    values.setdefault("cycle_log1p", math.log1p(req.cycle_index))
    missing = [name for name in names if values.get(name) is None]
    row = np.array([[values.get(name, np.nan) for name in names]], dtype=float)
    transformed = scaler.transform(imputer.transform(row)).astype(np.float32)
    features = torch.from_numpy(transformed)
    cycle = torch.tensor([req.cycle_index], dtype=torch.float32)
    with torch.inference_mode():
        seeds = [float(model(features, cycle).item()) for model in models]
    mean = float(np.mean(seeds))
    dispersion = float(np.std(seeds))
    empirical = read_json(BASE / "empirical_parameters.json")
    reference = empirical["c"] - empirical["a_sqrt_cycle"] * math.sqrt(req.cycle_index) - empirical["b_cycle"] * req.cycle_index
    return {
        "case_id": req.case_id,
        "cycle_index": req.cycle_index,
        "learned_soh_mean": mean,
        "learned_soh_seed_predictions": dict(zip((13, 42, 77), seeds)),
        "ensemble_dispersion": dispersion,
        "empirical_soh_reference": reference,
        "learned_minus_empirical": mean - reference,
        "feature_completeness": "complete" if not missing else "imputed",
        "missing_features": missing,
        "warning": None if not missing else "Missing inputs were filled by the benchmark median imputer.",
        "model_version": "physics-regularized-mlp-ensemble/benchmark-2026",
        "research_scope": "SOH research estimate; not safety, RUL, or certified BMS output.",
    }
