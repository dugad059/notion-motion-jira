import os
import requests
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load environment variables from .env file
load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate_google():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '.venv/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def retrieve_notion_tasks():
    try:
        filter_criteria = {
            "filter": {
                "and": [
                    {
                        "property": "MOVE",
                        "checkbox": {
                            "equals": True
                        }
                    },
                    {
                        "property": "IN",
                        "checkbox": {
                            "equals": False
                        }
                    }
                ]
            }
        }

        url = f"https://api.notion.com/v1/databases/{os.getenv('notion_database_id')}/query"

        headers = {
            'Authorization': f"Bearer {os.getenv('notion_integration_token')}",
            'Content-Type': 'application/json',
            'Notion-Version': '2022-06-28',
        }

        response = requests.post(url, headers=headers, json=filter_criteria)

        response.raise_for_status()  # Raises error for non-200 status codes

        data = response.json()
        tasks = []

        for item in data.get('results', []):
            task_id = item['id']  # Retrieve Notion task ID
            task_name = item['properties']['Task']['title'][0]['text']['content']
            duration_property = item['properties'].get('duration*')
            duration1 = duration_property['select']['name'] if duration_property and duration_property.get(
                'select') else 'No Duration'
            priority1 = item['properties']['Priority*']['status']['name']
            schedule_property = item['properties'].get('schedule*')
            schedule1 = schedule_property['select']['name'] if schedule_property and schedule_property.get(
                'select') else 'No Schedule'
            project_property = item['properties'].get('project*')
            project1 = project_property['select']['name'] if project_property and project_property.get(
                'select') else 'No Project'
            start_date_property = item['properties'].get('Start*')
            start_date1 = datetime.strptime(start_date_property['date']['start'],
                                             "%Y-%m-%d").date() if start_date_property and start_date_property.get(
                'date') else None
            due_date_property = item['properties'].get('Due*')
            due_date1 = datetime.strptime(due_date_property['date']['start'],
                                           "%Y-%m-%d").date() if due_date_property and due_date_property.get(
                'date') else None

            if due_date1:
                start_time = datetime.combine(due_date1, datetime.strptime('07:00:00', '%H:%M:%S').time())
                end_time = start_time + timedelta(hours=1)

                start_date = start_time.isoformat()
                end_date = end_time.isoformat()

                task = {
                    'summary': task_name,
                    'description': f"Priority: {priority1}\nDuration: {duration1}\nSchedule: {schedule1}\nProject: {project1}",
                    'start': {
                        'dateTime': start_date,
                        'timeZone': 'America/New_York',
                    },
                    'end': {
                        'dateTime': end_date,
                        'timeZone': 'America/New_York',
                    },
                    'visibility': 'private',
                    'notion_task_id': task_id  # Include the Notion task ID in the task object
                }
                tasks.append(task)

        return tasks

    except requests.exceptions.RequestException as e:
        print("An error occurred with the request:", e)
        return None

    except Exception as e:
        print("An unexpected error occurred:", e)
        return None

def update_notion_checkbox(notion_task_id):
    try:
        url = f"https://api.notion.com/v1/pages/{notion_task_id}"

        headers = {
            'Authorization': f"Bearer {os.getenv('notion_integration_token')}",
            'Content-Type': 'application/json',
            'Notion-Version': '2022-06-28',
        }

        data = {
            "properties": {
                "IN": {
                    "checkbox": True  # Set the checkbox to True
                }
            }
        }

        response = requests.patch(url, headers=headers, json=data)

        response.raise_for_status()  # Raises error for non-200 status codes

        print("Checkbox 'IN' updated successfully in Notion.")

    except requests.exceptions.RequestException as e:
        print("An error occurred with the request:", e)

    except Exception as e:
        print("An unexpected error occurred:", e)

def add_tasks_to_google_calendar(tasks):
    credentials = authenticate_google()
    service = build('calendar', 'v3', credentials=credentials)

    for task in tasks:
        try:
            event = service.events().insert(calendarId='', body=task).execute()
            print(f"Event created for task: {task['summary']}")
            print(f"Event date: {task['start']['dateTime']}")
            update_notion_checkbox(task['notion_task_id'])  # Call the function to update Notion checkbox
        except Exception as e:
            print(f"An error occurred while creating the event: {e}")

notion_tasks = retrieve_notion_tasks()
if notion_tasks:
    add_tasks_to_google_calendar(notion_tasks)














