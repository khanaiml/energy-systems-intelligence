# Deployment

Use Python 3.11/3.12 and Node 20+. Install pinned backend requirements in `backend/.venv`, run Uvicorn on port 8000, install frontend dependencies with `npm install`, and run Next.js on port 3000. `scripts/run_local.ps1` performs these starts after dependencies exist. Docker Compose uses CPU-only services and a persistent SQLite volume. Do not expose the research service publicly without authentication, TLS, origin restrictions, and operational review.
