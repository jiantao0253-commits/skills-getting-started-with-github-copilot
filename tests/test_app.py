import pytest
from fastapi.testclient import TestClient

from src.app import app


@pytest.fixture()
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_unregister_participant_removes_email_from_activity(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{email}")
    updated = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity_name}"
    assert email not in updated.json()[activity_name]["participants"]

    # Restore state for later tests
    client.post(f"/activities/{activity_name}/signup?email={email}")
