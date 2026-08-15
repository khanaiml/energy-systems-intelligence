from __future__ import annotations

import json
from functools import lru_cache

import joblib
import numpy as np
import pandas as pd

from .core import ARTIFACTS, DATA


FEATURES = ["hour", "day_of_week", "weekend", "month", "temperature", "humidity", "lag_1", "lag_24", "lag_48", "lag_168", "rolling_mean_24", "rolling_mean_168", "rolling_std_24"]


def make_features(frame: pd.DataFrame) -> pd.DataFrame:
    out = frame.copy()
    ts = pd.to_datetime(out["timestamp"])
    out["hour"] = ts.dt.hour
    out["day_of_week"] = ts.dt.dayofweek
    out["weekend"] = (ts.dt.dayofweek >= 5).astype(int)
    out["month"] = ts.dt.month
    load = out["load_kw"]
    for lag in (1, 24, 48, 168):
        out[f"lag_{lag}"] = load.shift(lag)
    shifted = load.shift(1)
    out["rolling_mean_24"] = shifted.rolling(24).mean()
    out["rolling_mean_168"] = shifted.rolling(168).mean()
    out["rolling_std_24"] = shifted.rolling(24).std()
    return out


@lru_cache
def artifacts():
    base = ARTIFACTS / "forecasting"
    return {name: joblib.load(base / file) for name, file in {"point":"point_model.joblib","p10":"quantile_p10.joblib","p50":"quantile_p50.joblib","p90":"quantile_p90.joblib"}.items()}


def day_ahead():
    frame = make_features(pd.read_csv(DATA / "forecast_history.csv")).dropna().reset_index(drop=True)
    rows = frame.tail(24)
    models = artifacts()
    pred = {key: model.predict(rows[FEATURES]) for key, model in models.items()}
    p10 = np.minimum(pred["p10"], pred["p50"])
    p90 = np.maximum(pred["p90"], pred["p50"])
    return [
        {
            "timestamp": row.timestamp,
            "actual_load_kw": float(row.load_kw),
            "p10": float(p10[position]),
            "p50": float(pred["p50"][position]),
            "p90": float(p90[position]),
        }
        for position, (_, row) in enumerate(rows.iterrows())
    ]


def metadata():
    return json.loads((ARTIFACTS / "forecasting" / "evaluation.json").read_text())
