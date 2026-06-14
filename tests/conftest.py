"""
Pytest fixtures for FastAPI application testing
"""

import pytest
import copy
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Provide a FastAPI TestClient"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities_state():
    """Reset activities to initial state before each test"""
    # Store original state
    original_state = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Practice team skills and compete in inter-school basketball games",
            "schedule": "Mondays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["liam@mergington.edu", "noah@mergington.edu"]
        },
        "Swimming Club": {
            "description": "Swim laps, learn techniques, and stay active in the pool",
            "schedule": "Tuesdays and Fridays, 3:00 PM - 4:15 PM",
            "max_participants": 20,
            "participants": ["ava@mergington.edu", "mia@mergington.edu"]
        },
        "Art Studio": {
            "description": "Explore painting, drawing, and mixed media art projects",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["harper@mergington.edu", "evelyn@mergington.edu"]
        },
        "Drama Society": {
            "description": "Rehearse and perform plays while developing acting skills",
            "schedule": "Tuesdays and Thursdays, 5:00 PM - 6:30 PM",
            "max_participants": 25,
            "participants": ["jackson@mergington.edu", "isabella@mergington.edu"]
        },
        "Debate Team": {
            "description": "Research important topics and compete in high school debates",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 16,
            "participants": ["ethan@mergington.edu", "amelia@mergington.edu"]
        },
        "Robotics Club": {
            "description": "Design, build, and program robots for competitions and challenges",
            "schedule": "Fridays, 4:00 PM - 6:00 PM",
            "max_participants": 14,
            "participants": ["lucas@mergington.edu", "zoe@mergington.edu"]
        }
    }
    
    # Clear current activities
    activities.clear()
    
    # Restore original state with deep copy to avoid mutations
    for key, value in original_state.items():
        activities[key] = copy.deepcopy(value)
    
    yield
    
    # Cleanup after test (optional, but good practice)
    activities.clear()
    for key, value in original_state.items():
        activities[key] = copy.deepcopy(value)
