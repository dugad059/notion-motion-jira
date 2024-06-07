import requests
import json
import urllib.parse
import os
from jira import get_assigned_jira_issues
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
sum_list = get_assigned_jira_issues()

# Define the Notion API URLs
url = f"https://api.notion.com/v1/databases/{os.getenv('notion_database_id')}/query"
url2 = f"https://api.notion.com/v1/pages"

# Headers containing the integration token
headers = {
    'Authorization': f"Bearer {os.getenv('notion_integration_token')}",
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28',  # Specify the Notion API version
}

def configure():
    load_dotenv()

def retrieve_tasks():
    configure()  # Load environment variables
    # Define the filter criteria
    filter_criteria = {
        "filter": {
            "and": [
            ]
        }
    }

    # Make a GET request to retrieve data from the database
    response = requests.post(url, headers=headers, json=filter_criteria)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse JSON response
        data = response.json()

        tasks = []

        # Extracting tasks and their attributes
        for item in data['results']:
            # TASK
            task_name = item['properties']['Task']['title'][0]['text']['content']
            tasks.append(task_name)

        return tasks
    else:
        print("Error:", response.status_code)


def filter_motion(sum_list, tasks):
    if tasks is None:
        print("There are no new tasks from Jira")
        return
    motion_list = []
    for variable in sum_list:
        if variable not in tasks:
            motion_list.append(variable)
    return motion_list


def create_tasks(motion_list):
    if motion_list is None:
        print("No tasks to create.")
        return
    
    # Initialize an empty list to store task_data dictionaries
    tasks = []

    # Iterate through each item in the list
    for item in motion_list:
        # Create a task_data dictionary for the current item
        task_data = {
            "parent": {"database_id": os.getenv('notion_database_id')},
            "properties": {
                "Task": {
                    "title": [
                        {
                            "text": {
                                "content": item  # Use the current item as the task title
                            }
                        }
                    ]
                }
            }
        }
        
        # Append the task_data dictionary to the list of tasks
        tasks.append(task_data)

    # Send the POST request to add each task
    for task_data in tasks:
        response = requests.post(url2, headers=headers, json=task_data)

        # Check if the request was successful
        if response.status_code == 200:
            task_name = task_data["properties"]["Task"]["title"][0]["text"]["content"]
            print(f"Task '{task_name}' added successfully to NOTION.")
        else:
            print("Failed to add task:", response.status_code)


# Execute all functions
tasks = retrieve_tasks()
motion_list = filter_motion(sum_list, tasks)
#create_tasks(motion_list)






