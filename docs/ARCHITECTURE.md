# Architecture

Executed battery benchmark → trusted TorchScript SOH ensemble → explicit current SOH → effective storage capacity. In parallel, UCI load plus Open-Meteo weather → leakage-safe point/quantile forecast and pvlib PV estimate → nine load/PV representations → hourly digital twin → deterministic/conservative/scenario-aware LP → persisted run, exports, API, and control-room dashboard.

Battery inference is deliberately isolated: microgrid power, SOC, tariff, and weather are never passed to the NASA model.
