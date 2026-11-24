# dev-homelab-platform

![CI](https://github.com/relitechsolutions/dev-homelab-platform/actions/workflows/ci.yml/badge.svg)

A FastAPI service that sits in front of a Proxmox VE cluster and exposes node and VM information through a clean REST API.

## Endpoints

| Method | Path | Description |
| --- | --- | --- |
| GET | `/health` | Liveness check |
| GET | `/nodes` | Cluster nodes with status, CPU and memory usage |
| GET | `/vms?node=<name>` | VMs on a node with status and memory |

Interactive API docs are served at `/docs` (Swagger UI) once the app is running.

## Configuration

The app reads two environment variables. Locally, put them in a `.env` file (it is gitignored and never committed):

```
PROXMOX_URL=https://<proxmox-host>:8006
PROXMOX_TOKEN=<user>@<realm>!<token-id>=<secret>
```

Use a read-only Proxmox API token.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Then open http://localhost:8000/docs.

## Tests and linting

```bash
ruff check .
pytest -v
```

Tests mock Proxmox calls, so they run without access to a cluster.

## CI

GitHub Actions runs lint and tests on every push to `main` and on every pull request. See [`.github/workflows/ci.yml`](.github/workflows/ci.yml).