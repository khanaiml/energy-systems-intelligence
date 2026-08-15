# Security and privacy

Trusted models load only from fixed repository paths. Pydantic rejects unknown feature fields and constrains batch/input sizes. No telemetry, analytics, paid API, or secrets are used. SQLite excludes raw NASA/UCI inputs. Downloads use fixed HTTPS endpoints, timeouts, caching, and recorded hashes. Production deployment should add authentication, TLS, rate limits, and stricter origin configuration.
