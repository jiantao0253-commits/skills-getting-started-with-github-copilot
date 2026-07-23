import pytest
from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity_name}"

    updated = client.get("/activities")
    assert email not in updated.json()[activity_name]["participants"]

    # restore state for later tests
    client.post(f"/activities/{activity_name}/signup?email={email}")
