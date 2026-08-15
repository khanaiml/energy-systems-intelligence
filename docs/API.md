# API

FastAPI exposes `/health`, system information, battery model info/single/batch estimates, forecast model info/day-ahead/evaluation, digital-twin simulation, dispatch config/optimize/compare, scenario list/detail/run, three evidence endpoints, run history/delete, and JSON/CSV exports under `/api/v1`. Interactive schemas and examples are available at `/docs` while the backend runs.

Example: `Invoke-RestMethod http://127.0.0.1:8000/api/v1/dispatch/optimize -Method Post -ContentType application/json -Body '{}'`.
