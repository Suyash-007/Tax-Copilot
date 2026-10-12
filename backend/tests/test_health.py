from fastapi.testclient import TestClient


def test_health_reports_schema_revision(client: TestClient) -> None:
    body = client.get("/api/health").json()
    assert body["status"] == "ok"
    assert body["schema_revision"] == "0001"
    assert body["llm_enabled"] is False


def test_rejects_non_loopback_host(client: TestClient) -> None:
    resp = client.get("/api/health", headers={"host": "evil.example.com"})
    assert resp.status_code == 400
