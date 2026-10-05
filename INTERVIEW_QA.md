# multi-mcp-cloudops-agent — interview questions and answers

[README](README.md) · [Project architecture](PROJECT_ARCHITECTURE.md)

Answers below use this repository’s files and implementation. They distinguish existing behavior from suggested extensions; source links let you verify each walkthrough.

## 1. What problem does multi-mcp-cloudops-agent address, and what can you demonstrate?

Agent → MCP → K8s / GCP / GitHub / Prometheus. Destructive ops need approved=true.

I would demonstrate the linked implementation or examples and distinguish that evidence from any planned production features. Start with [`README.md`](README.md).

## 2. How is this repository organized?

- [`src/mcpx/main.py`](src/mcpx/main.py): Implementation or supporting configuration.
- [`src/mcpx/mcp.py`](src/mcpx/mcp.py): Implementation or supporting configuration.
- [`requirements.txt`](requirements.txt): Implementation or supporting configuration.
- [`tests/test_mcp.py`](tests/test_mcp.py): Executable checks and regression examples.
- [`.github/workflows/ci.yml`](.github/workflows/ci.yml): GitHub Actions job definitions.
- [`README.md`](README.md): Project explanations or operating notes.

[PROJECT_ARCHITECTURE.md](PROJECT_ARCHITECTURE.md) contains the component diagram and the implementation walkthrough.

## 3. Can you walk through `call` and explain the decision it makes?

The main walkthrough here is `call(name, arguments, approved=False)` in [`src/mcpx/mcp.py`](src/mcpx/mcp.py#L4).

```python
def call(name, arguments, approved=False):
    if name not in TOOLS:
        raise ValueError("unknown tool")
    blob = str(arguments).lower() + name
    destructive = any(w in blob for w in ("apply", "delete", "destroy", "kubectl apply"))
    if destructive and not approved:
        return {"ok": False, "needs_approval": True, "applied": False}
    return {"ok": True, "tool": name, "echo": arguments or {}, "applied": False}
```

The implementation calls `ValueError`, `any`, `str`, `str(arguments).lower`. In an interview, trace those calls in execution order using a fixture input.

## 4. What responsibility does `list_tools` have?

`list_tools()` is defined in [`src/mcpx/mcp.py`](src/mcpx/mcp.py#L2).

Its return expressions include:

- `{'tools': TOOLS}`

## 5. What input validation and failure behavior are implemented?

Explicit failure paths include:

- `HTTPException(422, str(exc))` in [`src/mcpx/main.py`](src/mcpx/main.py#L18).
- `ValueError('unknown tool')` in [`src/mcpx/mcp.py`](src/mcpx/mcp.py#L6).

I would test both the condition that reaches each exception and the caller that translates it. An explicit raise does not mean every malformed input or dependency failure is handled.

## 6. Which test would you use to demonstrate correctness?

[`tests/test_mcp.py`](tests/test_mcp.py#L5) contains `test_allow_and_approval`:

```python
def test_allow_and_approval():
    assert "k8s.get_pods" in client.get("/tools").json()["tools"]
    assert client.post("/call", json={"name": "k8s.get_pods", "arguments": {"q": "status"}}).json()["ok"] is True
    blocked = client.post("/call", json={"name": "k8s.get_pods", "arguments": {"cmd": "kubectl apply"}}).json()
    assert blocked["needs_approval"] is True and blocked["applied"] is False
```

This is a concrete regression example from the repository. Its assertions establish that case; they do not establish behavior for every input or under production load.

## 7. What HTTP interface does the code expose?

- `GET /healthz` → `healthz` in [`src/mcpx/main.py`](src/mcpx/main.py#L6).
- `GET /tools` → `tools` in [`src/mcpx/main.py`](src/mcpx/main.py#L10).
- `POST /call` → `post_call` in [`src/mcpx/main.py`](src/mcpx/main.py#L14).

These are literal decorators. Application/router prefixes, authentication, and middleware must be checked in the corresponding setup code.

## 8. Where does state live, and what happens with multiple workers?

Module-level containers include `TOOLS` in [`src/mcpx/mcp.py`](src/mcpx/mcp.py).

These containers belong to a Python process. Inspect which are constant fixtures and which are mutated. Mutable process state needs an explicit shared-storage or synchronization strategy before multiple workers can provide consistent behavior.

## 9. How would another engineer reproduce your walkthrough?

Start from the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
```

These commands follow repository manifests; environment setup and command results still need to be checked on the target machine.

## 10. What does automation verify, and what does it not prove?

Inspect [`.github/workflows/ci.yml`](.github/workflows/ci.yml) for triggers, permissions, and job commands. I would name the checks that those definitions run and show the latest run separately. A workflow definition alone does not establish a successful deployment, security review, or production SLO.

## 11. How would you present this project in a Forward Deployed Engineer interview?

Start with the user and operational problem described in [`README.md`](README.md). Explain one constraint that changes the implementation, show the linked code or example, and walk through a success case and a failure case. Agree on a measurable acceptance criterion before expanding the solution, and leave a handoff with data boundaries and rollback ownership. Any proposed production or business metric should be identified as a target until measured.

## 12. What is the input-to-output contract of `call`?

In [`src/mcpx/mcp.py`](src/mcpx/mcp.py#L4), `call(name, arguments, approved=False)` receives the inputs. The function computes these intermediate values:

- `blob = str(arguments).lower() + name`
- `destructive = any((w in blob for w in ('apply', 'delete', 'destroy', 'kubectl apply')))`

Its result is defined by:

- `{'ok': True, 'tool': name, 'echo': arguments or {}, 'applied': False}`
- `{'ok': False, 'needs_approval': True, 'applied': False}`

## 13. Which decision rules or boundary conditions should an interviewer challenge?

The implementation in [`src/mcpx/mcp.py`](src/mcpx/mcp.py#L4) branches on:

- `name not in TOOLS`
- `destructive and (not approved)`

A useful extension is a table-driven test that covers each condition just below, at, and above its boundary where applicable. These expressions are the current rules; changing them changes behavior and should be justified by the project’s acceptance criteria.
