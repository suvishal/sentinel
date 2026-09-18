from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_create_log():
    response = client.post(
        "/logs",
        json={
            "level": "ERROR",
            "service": "test-service",
            "message": "Test log message"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["level"] == "ERROR"
    assert data["service"] == "test-service"
    assert data["message"] == "Test log message"
    assert data["id"] is not None
    assert data["timestamp"] is not None
    assert data["request_id"] is not None


def test_get_logs():
    response = client.get("/logs")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0

def test_create_log_validation():
    response = client.post(
        "/logs",
        json={
            "level": "NOT_A_LEVEL",
            "service": "",
            "message": ""
        }
    )

    assert response.status_code == 422