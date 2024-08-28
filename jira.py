import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv

load_dotenv()


def get_assigned_jira_issues():
    try:
        # Set up authentication
        auth = HTTPBasicAuth("david.dugas@webpt.com", "")
        headers = {
            "Accept": "application/json"
        }

        # Define the assignee display name
        assignee_display_name = "David Dugas"

        # Construct the JQL query to filter by project, assignee display name, issue types, and status
        jql_query = f'project={os.getenv("jira_project_key")} AND assignee="{assignee_display_name}" AND status in ("Waiting for Approval", "In Progress", "Pending", "Waiting For Support", "Waiting For Customer")'

        # Construct the endpoint URL with the modified JQL query
        endpoint = f"{os.getenv('jira_base_url')}/rest/api/3/search?jql={jql_query}&maxResults=1000"

        # Get the issues assigned to the specified user
        response = requests.get(endpoint, headers=headers, auth=auth)
        response.raise_for_status()  # Raise an exception for HTTP errors (status code >= 400)
        issues_data = response.json()

        sum_list = []

        # Extract information for each issue
        for issue in issues_data['issues']:
            summary = issue['fields']['summary']
            sum_list.append(summary)

        return sum_list

    except requests.exceptions.RequestException as e:
        # Handle network-related errors
        print("Error occurred:", e)
        return None

    except KeyError as e:
        # Handle unexpected response format
        print("Error: Unexpected response format. Key not found:", e)
        return None

    except Exception as e:
        # Handle other unexpected errors
        print("An unexpected error occurred:", e)
        return None


assigned_issues = get_assigned_jira_issues()

# Example usage:
#if assigned_issues:
 #   for issue_summary in assigned_issues:
  #      print(issue_summary)




