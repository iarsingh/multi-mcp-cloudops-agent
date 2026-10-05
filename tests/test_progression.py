from mcpx.progression import mcp_cloud

def test_mcp_cloud_refuses_apply_even_when_approved():
    out = mcp_cloud("tf.apply", {"stack": "prod"}, approved=True)
    assert out["applied"] is False

