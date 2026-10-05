# Multi-MCP CloudOps Agent

<!-- project-guide:start -->
## Project guide

[Project architecture](PROJECT_ARCHITECTURE.md) · [Interview questions and answers](INTERVIEW_QA.md)

Use the architecture document for the component diagram, implementation boundaries, and verification entry points. The interview guide includes source-backed answers and project walkthroughs.

### Implementation map

| Component | Responsibility |
| --- | --- |
| [`src/mcpx/main.py`](src/mcpx/main.py) | HTTP handlers: `GET /healthz`, `GET /tools`, `POST /call` |
| [`src/mcpx/mcp.py`](src/mcpx/mcp.py) | Functions: `list_tools`, `call` |
| [`requirements.txt`](requirements.txt) | Implementation or supporting configuration |
| [`tests/test_mcp.py`](tests/test_mcp.py) | Executable checks and regression examples |
| [`.github/workflows/ci.yml`](.github/workflows/ci.yml) | GitHub Actions job definitions |
| [`README.md`](README.md) | Project explanations or operating notes |

### Local setup and verification

From the repository root (the commands follow the checked-in manifests):

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
```

To serve the FastAPI application locally, install the server separately if it is not already available:

```bash
python -m pip install uvicorn
PYTHONPATH=src python -m uvicorn mcpx.main:app --reload
```

<!-- project-guide:end -->

Phase 5

Skills: MCP Kubernetes, GCP, GitHub, Prometheus

Agent → MCP → K8s / GCP / GitHub / Prometheus. Destructive ops need approved=true.

```bash
pip install -r requirements.txt
pytest -q
```

Laptop proof. No hosted model. Cluster apply stays false until a human approves.
