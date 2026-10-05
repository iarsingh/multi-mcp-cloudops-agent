from mcpx.ops import router as ops_router
from fastapi import FastAPI, HTTPException
from mcpx.mcp import call, list_tools
app = FastAPI()
app.include_router(ops_router, prefix="/v1")

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.get("/tools")
def tools():
    return list_tools()

@app.post("/call")
def post_call(body: dict):
    try:
        return call(body.get("name"), body.get("arguments"), body.get("approved", False))
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc
