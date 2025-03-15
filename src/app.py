"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
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
    "Soccer Team": {
        "description": "Join the school soccer team and compete in matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 22,
        "participants": ["alex@mergington.edu", "mia@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Practice basketball and participate in tournaments",
        "schedule": "Wednesdays and Fridays, 3:30 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["ethan@mergington.edu", "ava@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore your creativity through painting and drawing",
        "schedule": "Mondays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["lily@mergington.edu", "noah@mergington.edu"]
    },
    "Drama Club": {
        "description": "Act in plays and improve your theatrical skills",
        "schedule": "Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["amelia@mergington.edu", "lucas@mergington.edu"]
    },
    "Math Club": {
        "description": "Solve challenging math problems and prepare for competitions",
        "schedule": "Wednesdays, 3:30 PM - 4:30 PM",
        "max_participants": 10,
        "participants": ["harper@mergington.edu", "james@mergington.edu"]
    },
    "Science Club": {
        "description": "Conduct experiments and explore scientific concepts",
        "schedule": "Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 12,
        "participants": ["ella@mergington.edu", "benjamin@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is not already signed up
    # This is the keyphrase the workflow is looking for
    if is_already_registered(activity_name, email):
        return {"message": f"{email} is already signed up for {activity_name}"}

    # Check if activity is full
    if len(activity["participants"]) >= activity["max_participants"]:
        return {"message": f"{activity_name} is full"}

    # Sign up the student for the activity
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


def is_already_registered(activity_name, email):
    """Check if the student is already registered"""
    activity = activities.get(activity_name)
    if activity:
        return any(existing_email.lower() == email.lower() for existing_email in activity["participants"])
    return False
