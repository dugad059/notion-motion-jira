import motion
import notion_motion


from motion import notion_dict



def main():

    #NOTION_MOTION
    notion_motion.retrieve_notion_tasks()

    #MOTION
    motion.create_tasks_in_motion(notion_dict)

   




if __name__ == "__main__":
    main()  