import requests
import os
from notion_motion import notion_dict
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


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

        for task in tasks_list:
            # Construct the request
            url = 'https://api.usemotion.com/v1/tasks'
            headers = {'X-API-Key': os.getenv('motion_api_key'), 'Content-Type': 'application/json'}
            response = requests.post(url, json=task, headers=headers)

            # Handle the response
            if response.status_code == 201:
                print('Task created successfully!')
            else:
                print('Error:', response.status_code)
                print(response.text)

    except Exception as e:
        print("An unexpected error occurred:", e)

# Example usage:
create_tasks_in_motion(notion_dict)