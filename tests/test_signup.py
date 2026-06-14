"""
Tests for POST /activities/{activity_name}/signup endpoint
"""

import pytest


def test_signup_new_student_success(client):
    """Test that a new student can successfully sign up for an activity"""
    email = "newstudent@mergington.edu"
    activity_name = "Chess Club"
    
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity_name in data["message"]


def test_signup_new_student_added_to_participants(client):
    """Test that a new student is actually added to the participants list"""
    email = "newstudent@mergington.edu"
    activity_name = "Chess Club"
    
    # Signup
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    assert response.status_code == 200
    
    # Verify via GET endpoint
    response = client.get("/activities")
    activities = response.json()
    chess_club_participants = activities["Chess Club"]["participants"]
    
    assert email in chess_club_participants
    assert len(chess_club_participants) == 3  # Was 2, now 3


def test_signup_activity_not_found(client):
    """Test that signup fails if activity doesn't exist"""
    email = "student@mergington.edu"
    activity_name = "Nonexistent Activity"
    
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_signup_duplicate_registration(client):
    """Test that a student cannot sign up twice for the same activity"""
    email = "michael@mergington.edu"  # Already signed up for Chess Club
    activity_name = "Chess Club"
    
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"]


def test_signup_multiple_activities(client):
    """Test that a student can sign up for multiple different activities"""
    email = "versatile@mergington.edu"
    
    # Sign up for Chess Club
    response1 = client.post(
        "/activities/Chess Club/signup",
        params={"email": email}
    )
    assert response1.status_code == 200
    
    # Sign up for Programming Class
    response2 = client.post(
        "/activities/Programming Class/signup",
        params={"email": email}
    )
    assert response2.status_code == 200
    
    # Verify both signups
    response = client.get("/activities")
    activities = response.json()
    
    assert email in activities["Chess Club"]["participants"]
    assert email in activities["Programming Class"]["participants"]


def test_signup_response_message_format(client):
    """Test that signup response has the correct message format"""
    email = "testmail@mergington.edu"
    activity_name = "Gym Class"
    
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    assert response.status_code == 200
    data = response.json()
    expected_message = f"Signed up {email} for {activity_name}"
    assert data["message"] == expected_message


def test_signup_special_characters_in_email(client):
    """Test that signup works with email containing special characters"""
    email = "john.doe+test@mergington.edu"
    activity_name = "Art Studio"
    
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    assert response.status_code == 200
    
    # Verify in participants
    response = client.get("/activities")
    activities = response.json()
    assert email in activities["Art Studio"]["participants"]
