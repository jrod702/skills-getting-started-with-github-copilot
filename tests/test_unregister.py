"""
Tests for DELETE /activities/{activity_name}/unregister endpoint
"""

import pytest


def test_unregister_registered_student_success(client):
    """Test that a registered student can be unregistered"""
    email = "michael@mergington.edu"  # Already in Chess Club
    activity_name = "Chess Club"
    
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity_name in data["message"]


def test_unregister_removes_from_participants(client):
    """Test that unregister actually removes the participant"""
    email = "michael@mergington.edu"
    activity_name = "Chess Club"
    
    # Verify participant is there before
    response = client.get("/activities")
    before = response.json()
    assert email in before["Chess Club"]["participants"]
    assert len(before["Chess Club"]["participants"]) == 2
    
    # Unregister
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    assert response.status_code == 200
    
    # Verify participant is gone after
    response = client.get("/activities")
    after = response.json()
    assert email not in after["Chess Club"]["participants"]
    assert len(after["Chess Club"]["participants"]) == 1


def test_unregister_activity_not_found(client):
    """Test that unregister fails if activity doesn't exist"""
    email = "student@mergington.edu"
    activity_name = "Nonexistent Activity"
    
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_unregister_student_not_registered(client):
    """Test that unregister fails if student is not registered"""
    email = "notregistered@mergington.edu"
    activity_name = "Chess Club"
    
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "not registered" in data["detail"]


def test_unregister_then_signup_again(client):
    """Test that a student can unregister and then sign up again"""
    email = "flip@mergington.edu"
    activity_name = "Programming Class"
    
    # First signup
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    assert response.status_code == 200
    
    # Unregister
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    assert response.status_code == 200
    
    # Sign up again
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    assert response.status_code == 200
    
    # Verify registered
    response = client.get("/activities")
    activities = response.json()
    assert email in activities["Programming Class"]["participants"]


def test_unregister_response_message_format(client):
    """Test that unregister response has the correct message format"""
    email = "michael@mergington.edu"
    activity_name = "Chess Club"
    
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    assert response.status_code == 200
    data = response.json()
    expected_message = f"Unregistered {email} from {activity_name}"
    assert data["message"] == expected_message


def test_unregister_special_characters_in_email(client):
    """Test that unregister works with special characters in email"""
    email = "jane.doe+special@mergington.edu"
    activity_name = "Swimming Club"
    
    # First signup with special chars
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    assert response.status_code == 200
    
    # Then unregister
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    assert response.status_code == 200
    
    # Verify removed
    response = client.get("/activities")
    activities = response.json()
    assert email not in activities["Swimming Club"]["participants"]


def test_unregister_multiple_students(client):
    """Test that unregistering one student doesn't affect others"""
    # Chess Club starts with michael and daniel
    michael = "michael@mergington.edu"
    daniel = "daniel@mergington.edu"
    
    # Unregister michael
    response = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": michael}
    )
    assert response.status_code == 200
    
    # Verify daniel is still there
    response = client.get("/activities")
    participants = response.json()["Chess Club"]["participants"]
    assert michael not in participants
    assert daniel in participants
