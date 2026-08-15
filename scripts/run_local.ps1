$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$backend = Join-Path $root 'backend'
$frontend = Join-Path $root 'frontend'
Start-Process -FilePath (Join-Path $backend '.venv\Scripts\python.exe') -ArgumentList '-m','uvicorn','app.main:app','--host','127.0.0.1','--port','8000' -WorkingDirectory $backend -WindowStyle Hidden
Start-Process -FilePath 'npm.cmd' -ArgumentList 'run','dev' -WorkingDirectory $frontend -WindowStyle Hidden
Write-Output 'Frontend http://localhost:3000 | API http://127.0.0.1:8000 | OpenAPI http://127.0.0.1:8000/docs'
