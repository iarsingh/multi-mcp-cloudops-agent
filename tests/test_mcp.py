from fastapi.testclient import TestClient
from mcpx.main import app
client = TestClient(app)

def test_allow_and_approval():
    assert "k8s.get_pods" in client.get("/tools").json()["tools"]
    assert client.post("/call", json={"name": "k8s.get_pods", "arguments": {"q": "status"}}).json()["ok"] is True
    blocked = client.post("/call", json={"name": "k8s.get_pods", "arguments": {"cmd": "kubectl apply"}}).json()
    assert blocked["needs_approval"] is True and blocked["applied"] is False
