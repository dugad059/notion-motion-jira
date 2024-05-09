import jira
import motion
import notion_jira
import notion_motion

from notion_jira import sum_list, tasks, motion_list
from motion import notion_dict



def main():
    #JIRA
    jira.get_assigned_jira_issues()

    #NOTION_JIRA
    notion_jira.retrieve_tasks()
    notion_jira.filter_motion(sum_list, tasks)
    notion_jira.create_tasks(motion_list)

    #NOTION_MOTION
    notion_motion.retrieve_notion_tasks()

    #MOTION
    motion.create_tasks_in_motion(notion_dict)

   




if __name__ == "__main__":
    main()    