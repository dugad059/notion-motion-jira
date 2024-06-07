import requests
import os
from notion_motion import retrieve_notion_tasks
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

# Retrieve Notion tasks
notion_dict = retrieve_notion_tasks()

# Function to update the 'IN' checkbox in Notion
def update_notion_task(task_id):
    try:
        url = f"https://api.notion.com/v1/pages/{task_id}"
        headers = {
            'Authorization': f"Bearer {os.getenv('notion_integration_token')}",
            'Content-Type': 'application/json',
            'Notion-Version': '2022-06-28',  # Specify the Notion API version
        }
        update_data = {
            "properties": {
                "IN": {
                    "checkbox": True
                }
            }
        }
        
        response = requests.patch(url, headers=headers, data=json.dumps(update_data))
        
        if response.status_code == 200:
            print(f'Task with ID {task_id} updated successfully in Notion!')
        else:
            print(f'Error updating task with ID {task_id} in Notion:', response.status_code)
            print(response.text)
            
    except Exception as e:
        print(f"An unexpected error occurred while updating Notion task with ID {task_id}:", e)

# Function to create tasks in Motion
def create_tasks_in_motion(notion_dict):
    try:
        tasks_list = []

        for i in range(len(notion_dict['tasks'])):
            task = {
                'name': notion_dict['tasks'][i],
                'dueDate': notion_dict['due'][i],
                'workspaceId': 'BRbMFt2509GdvgJ3zciiP',  # Workspace ID
                'projectId': 'EzMDWbV5sE4-lh6_LpXhU',  # Project ID
                'priority': notion_dict['priority'][i],
                'autoScheduled': {
                    'startDate': notion_dict['start'][i],
                    'deadlineType': 'SOFT',
                    'schedule': notion_dict['schedule'][i]
                }
            }
            tasks_list.append(task)

        for i, task in enumerate(tasks_list):
            # Construct the request
            url = 'https://api.usemotion.com/v1/tasks'
            headers = {'X-API-Key': os.getenv('motion_api_key'), 'Content-Type': 'application/json'}
            response = requests.post(url, json=task, headers=headers)

            # Handle the response
            if response.status_code == 201:
                print(f'Task "{task["name"]}" created successfully in MOTION!')
                # Get the corresponding Notion task ID and update the 'IN' checkbox
                notion_task_id = notion_dict['ids'][i]
                update_notion_task(notion_task_id)
            else:
                print('Error:', response.status_code)
                print(response.text)

    except Exception as e:
        print("An unexpected error occurred:", e)

# Execute the task creation only once
#if notion_dict:
    #create_tasks_in_motion(notion_dict)



