from __future__ import annotations

import numpy as np
import pandas as pd
import pvlib


def pv_estimate(weather: pd.DataFrame, capacity_kw=12.0, tilt=30.0, azimuth=180.0, inverter_efficiency=0.96, losses=0.14):
    times = pd.DatetimeIndex(pd.to_datetime(weather["timestamp"], utc=True))
    solpos = pvlib.solarposition.get_solarposition(times, 48.78, 2.29)
    dni = weather.get("dni", pd.Series(np.zeros(len(weather)))).clip(lower=0).to_numpy()
    ghi = weather["shortwave_radiation"].clip(lower=0).to_numpy()
    dhi = weather.get("diffuse_radiation", pd.Series(np.maximum(ghi - dni * np.cos(np.radians(solpos["zenith"])), 0))).clip(lower=0).to_numpy()
    poa = pvlib.irradiance.get_total_irradiance(tilt, azimuth, solpos["zenith"], solpos["azimuth"], dni, ghi, dhi)["poa_global"].fillna(0).clip(lower=0)
    return (capacity_kw * poa.to_numpy() / 1000 * inverter_efficiency * (1 - losses)).clip(0, capacity_kw)
