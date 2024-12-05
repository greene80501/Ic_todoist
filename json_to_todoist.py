from todoist_api_python.api import TodoistAPI
import json
from datetime import datetime

# Your Todoist API token
TODOIST_API_TOKEN = '819a0da713c875c3b55303f1ac4febe16553ddea'

# Path to the JSON file
json_file_path = "assignments.json"

# Initialize Todoist API client
api = TodoistAPI(TODOIST_API_TOKEN)

# Open and load the JSON data
with open(json_file_path, "r") as file:
    data = json.load(file)

# Function to check if a task already exists
def task_exists(existing_tasks, task_name):
    # Convert task_name to lowercase for case-insensitive comparison
    task_name = task_name.lower()
    for task in existing_tasks:
        if task.content.lower() == task_name:
            return True
    return False

# Retrieve all existing tasks
try:
    existing_tasks = api.get_tasks()
except Exception as e:
    print(f"An error occurred while retrieving tasks: {e}")
    existing_tasks = []

# Check if data is a list
if isinstance(data, list):
    # Iterate over each assignment and process it
    for assignment in data:
        # Get assignment details
        assignment_name = assignment.get('assignmentName', 'N/A')
        due_date = assignment.get('dueDate', 'N/A')
        course_name = assignment.get('courseName', 'N/A')
        score = assignment.get('score')
        score_points = assignment.get('scorePoints', 'N/A')
        missing = assignment.get('missing', False)  # Check if "missing" field exists

        # Skip tasks that are missing or don't have a due date
        if missing or not due_date:
            print(f"Skipping '{assignment_name}' because it's marked as missing or has no due date.")
            continue

        # Convert due_date to datetime object
        try:
            due_date_obj = datetime.strptime(due_date, '%Y-%m-%dT%H:%M:%S.%fZ')
        except ValueError:
            print(f"Invalid date format for assignment '{assignment_name}'. Skipping...")
            continue

        # Check if the due date is today or in the future
        if due_date_obj.date() < datetime.today().date():
            print(f"Skipping '{assignment_name}' because the due date is in the past.")
            continue

        # Only add if the task does not already exist
        if not task_exists(existing_tasks, assignment_name):
            try:
                task = api.add_task(
                    content=assignment_name,  # Task name
                    due_string=due_date,  # Due date as a string
                    description=f"{course_name} {score_points}"  # Additional information about course and points
                )
                print(f"Task created: {task}")
            except Exception as e:
                print(f"An error occurred: {e}")
        else:
            print(f"Task '{assignment_name}' already exists. Skipping...")
else:
    print("The JSON data is not in the expected format.")
