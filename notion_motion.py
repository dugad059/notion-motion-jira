import requests
import json
import urllib.parse
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def retrieve_notion_tasks():
    try:
        # Define the filter criteria
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

        # URL for retrieving database contents
        url = f"https://api.notion.com/v1/databases/{os.getenv('notion_database_id')}/query"

        # Headers containing the integration token
        headers = {
            'Authorization': f"Bearer {os.getenv('notion_integration_token')}",
            'Content-Type': 'application/json',
            'Notion-Version': '2022-06-28',  # Specify the Notion API version
        }

        # Make a GET request to retrieve data from the database
        response = requests.post(url, headers=headers, json=filter_criteria)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse JSON response
            data = response.json()

            tasks = []
            duration = []
            priority = []
            due = []
            start = []
            schedule = []
            project = []
            notion_dict = {}

            # Extracting tasks and their attributes
            for item in data['results']:
                # TASK
                task_name = item['properties']['Task']['title'][0]['text']['content']
                tasks.append(task_name)

                # DURATION
                duration_property = item['properties'].get('duration*')
                duration1 = duration_property['select']['name'] if duration_property and duration_property.get('select') else 'No Duration'
                duration.append(duration1)

                # PRIORITY
                priority1 = item['properties']['Priority*']['status']['name']
                priority.append(priority1)

                # DUE DATE
                due_date_property = item['properties'].get('Due*')
                due_date = due_date_property['date']['start'] if due_date_property and due_date_property.get('date') else 'No Due Date'
                due.append(due_date)

                # START DATE
                start_date_property = item['properties'].get('Start*')
                start_date = start_date_property['date']['start'] if start_date_property and start_date_property.get('date') else 'No Start Date'
                start.append(start_date)

                # SCHEDULE
                schedule_property = item['properties'].get('schedule*')
                schedule1 = schedule_property['select']['name'] if schedule_property and schedule_property.get('select') else 'No Schedule'
                schedule.append(schedule1)

                # PROJECT
                project_property = item['properties'].get('project*')
                project1 = project_property['select']['name'] if project_property and project_property.get('select') else 'No Project'
                project.append(project1)

        else:
            print("Error:", response.status_code)
            return None

        notion_dict['tasks'] = tasks
        notion_dict['duration'] = duration
        notion_dict['priority'] = priority
        notion_dict['due'] = due
        notion_dict['start'] = start
        notion_dict['schedule'] = schedule
        notion_dict['project'] = project

        return notion_dict

    except Exception as e:
        print("An unexpected error occurred:", e)
        return None


notion_tasks = retrieve_notion_tasks()


# Example usage:
#if notion_tasks:
    #print(notion_tasks)
