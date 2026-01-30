from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # Ensure a known activity exists
    assert "Basketball Team" in data


def test_signup_and_unregister_flow():
    activity = "Basketball Team"
    email = "teststudent@mergington.edu"

    # Ensure email not already in participants
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Sign up
    signup_resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup_resp.status_code == 200
    assert signup_resp.json()["message"].startswith("Signed up")
    assert email in activities[activity]["participants"]

    # Duplicate signup should fail
    dup_resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert dup_resp.status_code == 400

    # Unregister
    unregister_resp = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert unregister_resp.status_code == 200
    assert unregister_resp.json()["message"].startswith("Unregistered")
    assert email not in activities[activity]["participants"]

    # Unregistering again should fail
    unregister_again = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert unregister_again.status_code == 400


def test_signup_nonexistent_activity():
    resp = client.post("/activities/NoSuchActivity/signup?email=foo@bar.com")
    assert resp.status_code == 404


def test_unregister_nonexistent_activity():
    resp = client.delete("/activities/NoSuchActivity/unregister?email=foo@bar.com")
    assert resp.status_code == 404
