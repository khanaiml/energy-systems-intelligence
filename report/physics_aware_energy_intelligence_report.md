# Physics-Aware Energy Intelligence

## Abstract

This platform links controlled battery SOH evidence to real public load/weather data, day-ahead forecast bands, weather-driven photovoltaic availability, hourly physical constraints, and dispatch optimization. It is a reproducible research and engineering demonstration, not operational control software.

## Battery Benchmark

The executed NASA benchmark contains 636 discharge cycles from four cells, 24 first-600-second features, leave-one-battery-out evaluation, four development fractions, and three seeds. Physics-regularized MLP leads full-data RMSE at 0.027193; the empirical curve leads at 10% data. Controlled contrasts show a positive median direct-MLP physics benefit but a negative worst case, preventing a universal claim.

## Forecasting Data and Models

The load reference is UCI ID 235 for Sceaux, processed hourly over January–March 2009 and joined with matching Open-Meteo history. Lag/rolling features are strictly past-looking. Chronological 70/15/15 evaluation gives learned test MAE 0.43148 kW and RMSE 0.60985 kW on the unscaled household reference; all exact baseline metrics are in the saved evaluation JSON. Quantile bands cover 78.26% of held-out observations.

## PV Estimation

The service uses pvlib solar position and irradiance transposition with configurable capacity, tilt, azimuth, inverter efficiency, and losses. Output is a physics-based reference estimate, not measured PV.

## Digital Twin

The hourly model represents load, PV, storage, grid connection, export, curtailment, and unserved slack. SOH transparently derates energy capacity; it does not infer hourly degradation. Charge/discharge efficiency and SOC limits govern energy state.

## Dispatch Formulation

HiGHS minimizes import less export revenue plus throughput, curtailment, unserved-energy, and terminal-deviation terms subject to exact hourly balance and component bounds. A validated base run is optimal with maximum energy-balance residual 8.88e-16 kWh; its objective is €173.86255 under the documented synthetic tariff and ×10 engineering scaling. This is a scenario result, not a savings claim.

## Uncertainty-Aware Optimization and Scenarios

The UI/API compare deterministic, conservative, and uncertainty-aware proxy strategies across eight input-defined cases. Outcomes are always solver-generated. A full shared-first-stage nine-scenario stochastic formulation remains future work and is not claimed here.

## Operations Platform

FastAPI provides versioned services, SQLite run persistence, and exports. Next.js provides the control-room shell and evidence views. Docker and CI definitions support reproducibility.

## Limitations

Small battery benchmark; cell-to-pack generalization unknown; ensemble spread uncalibrated; one-household load reference and engineered scaling; short demo period; historical weather and estimated PV; simplified hourly model; synthetic tariff; continuous LP; no certified safety/control claims.

## Conclusion

The repository demonstrates a coherent benchmark → forecast → simulate → optimize → operate workflow while keeping measured evidence, engineering assumptions, and scientific boundaries explicit.

## References

NASA Ames PCoE Li-ion Battery Aging Dataset. UCI Individual Household Electric Power Consumption (DOI 10.24432/C58K54). Open-Meteo Historical Weather API. pvlib Python. SciPy HiGHS.
