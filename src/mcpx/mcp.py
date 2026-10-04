TOOLS = ["k8s.get_pods", "gcp.describe", "github.workflow", "prom.query"]
def list_tools():
    return {"tools": TOOLS}
def call(name, arguments, approved=False):
    if name not in TOOLS:
        raise ValueError("unknown tool")
    blob = str(arguments).lower() + name
    destructive = any(w in blob for w in ("apply", "delete", "destroy", "kubectl apply"))
    if destructive and not approved:
        return {"ok": False, "needs_approval": True, "applied": False}
    return {"ok": True, "tool": name, "echo": arguments or {}, "applied": False}
