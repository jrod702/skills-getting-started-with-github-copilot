"""
Tests for GET /activities endpoint
"""

import pytest


def test_get_activities_returns_all_activities(client):
    """Test that GET /activities returns all available activities"""
    response = client.get("/activities")
    
    assert response.status_code == 200
    activities = response.json()
    
    # Check that all expected activities are present
    expected_activities = [
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Basketball Team",
        "Swimming Club",
        "Art Studio",
        "Drama Society",
        "Debate Team",
        "Robotics Club"
    ]
    
    for activity in expected_activities:
        assert activity in activities, f"Missing activity: {activity}"


def test_activity_structure(client):
    """Test that each activity has the correct structure"""
    response = client.get("/activities")
    activities = response.json()
    
    # Check first activity structure
    chess_club = activities["Chess Club"]
    
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club
    
    assert isinstance(chess_club["description"], str)
    assert isinstance(chess_club["schedule"], str)
    assert isinstance(chess_club["max_participants"], int)
    assert isinstance(chess_club["participants"], list)


def test_activity_has_participants(client):
    """Test that activities have participant information"""
    response = client.get("/activities")
    activities = response.json()
    
    chess_club = activities["Chess Club"]
    
    # Should have 2 participants initially
    assert len(chess_club["participants"]) == 2
    assert "michael@mergington.edu" in chess_club["participants"]
    assert "daniel@mergington.edu" in chess_club["participants"]


def test_activity_availability_calculation(client):
    """Test that we can calculate availability from max_participants and participants"""
    response = client.get("/activities")
    activities = response.json()
    
    gym_class = activities["Gym Class"]
    
    # Gym Class has max 30 participants and 2 registered
    spots_left = gym_class["max_participants"] - len(gym_class["participants"])
    assert spots_left == 28


def test_activities_count(client):
    """Test that the correct number of activities are returned"""
    response = client.get("/activities")
    activities = response.json()
    
    # Should have exactly 9 activities
    assert len(activities) == 9
