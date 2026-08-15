# Energy Systems Intelligence

Battery health, probabilistic forecasting, microgrid simulation, and uncertainty-aware dispatch.

This local-first research platform connects an executed NASA battery SOH benchmark to a real UCI household load reference, Open-Meteo weather, physics-based PV availability, an hourly microgrid digital twin, and constrained operational decisions. Prediction is evidence for a decision—not the final output.

## Evidence at a glance

| Layer | Implemented evidence |
|---|---|
| Battery | 636 cycles, 4 held-out batteries, 24 features; Physics-regularized MLP full-data RMSE 0.02719 |
| Forecast | Real UCI ID 235 window; chronological 70/15/15 split; learned model plus three baselines |
| Uncertainty | P10/P50/P90 forecast bands; measured P10–P90 test coverage 78.26% |
| PV | Weather-driven pvlib transposition and configurable system losses |
| Dispatch | HiGHS LP with energy balance, SOC, power, grid, outage, and terminal constraints |

Physics regularization improved the matched direct MLP overall and produced the strongest full-data cross-battery result, but the gain was not universal. The empirical degradation curve remained strongest at the extreme 10% data setting, and sequence-physics penalties did not improve the matched hybrid architecture.

## Start locally

```powershell
cd backend
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

```powershell
cd frontend
npm install
npm run dev
```

Frontend: `http://localhost:3000` · API: `http://127.0.0.1:8000` · OpenAPI: `http://127.0.0.1:8000/docs`

The packaged demo works offline after installation. Full raw UCI data is excluded; acquisition scripts reproduce the committed processed window. See `docs/` and the integrated report for methods, validation, limitations, licenses, and API contracts.

> Research and engineering demonstration only. Not a certified battery-management system, utility controller, grid-protection system, safety system, or trading system.
