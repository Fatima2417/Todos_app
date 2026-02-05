"""
Todo In-Memory Python Console App
Main application entry point
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from models.task import (
    add_task, get_all_tasks, update_task, delete_task,
    toggle_task_completion, reset_storage
)
from utils.cli_helpers import (
    display_menu, display_tasks, get_validated_input,
    get_positive_int_input, confirm_action
)


def main():
    """Main function to run the todo app"""
    print("Welcome to the Todo In-Memory Python Console App!")

    # Define menu options
    menu_options = [
        "Add Task",
        "Delete Task",
        "Update Task",
        "View Task List",
        "Mark Task Complete/Incomplete",
        "Exit"
    ]

    # Main menu loop
    while True:
        display_menu(menu_options)

        try:
            choice = get_positive_int_input("Select an option (1-6): ")

            if choice == 1:
                add_task_handler()
            elif choice == 2:
                delete_task_handler()
            elif choice == 3:
                update_task_handler()
            elif choice == 4:
                view_tasks_handler()
            elif choice == 5:
                toggle_completion_handler()
            elif choice == 6:
                print("Thank you for using the Todo App. Goodbye!")
                break
            else:
                print("Invalid choice. Please select a number between 1 and 6.")

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")


def add_task_handler():
    """Handle adding a new task"""
    try:
        title = input("Enter task title: ").strip()
        if not title:
            print("Task title cannot be empty.")
            return

        description = input("Enter task description (optional, press Enter to skip): ").strip()

        task = add_task(title, description)
        print(f"Task '{task['title']}' added successfully with ID {task['id']}!")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def delete_task_handler():
    """Handle deleting a task"""
    try:
        task_list = get_all_tasks()
        if not task_list:
            print("No tasks available to delete.")
            return

        display_tasks(task_list)
        task_id = get_positive_int_input("Enter the ID of the task to delete: ")

        # Verify the task exists before attempting deletion
        if not any(task['id'] == task_id for task in task_list):
            print(f"No task found with ID {task_id}.")
            return

        confirmed = confirm_action(f"Are you sure you want to delete task {task_id}?")
        if confirmed:
            if delete_task(task_id):
                print(f"Task with ID {task_id} deleted successfully!")
            else:
                print(f"Failed to delete task with ID {task_id}.")
        else:
            print("Deletion cancelled.")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def update_task_handler():
    """Handle updating a task"""
    try:
        task_list = get_all_tasks()
        if not task_list:
            print("No tasks available to update.")
            return

        display_tasks(task_list)
        task_id = get_positive_int_input("Enter the ID of the task to update: ")

        # Verify the task exists
        task = next((task for task in task_list if task['id'] == task_id), None)
        if not task:
            print(f"No task found with ID {task_id}.")
            return

        # Get new values (or keep current ones if no input provided)
        print(f"Current title: {task['title']}")
        new_title = input("Enter new title (press Enter to keep current): ").strip()
        new_title = new_title if new_title else task['title']

        print(f"Current description: {task['description']}")
        new_desc = input("Enter new description (press Enter to keep current): ").strip()
        new_desc = new_desc if new_desc else task['description']

        if update_task(task_id, new_title, new_desc):
            print(f"Task with ID {task_id} updated successfully!")
        else:
            print(f"Failed to update task with ID {task_id}.")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def view_tasks_handler():
    """Handle viewing the task list"""
    try:
        task_list = get_all_tasks()
        display_tasks(task_list)

    except Exception as e:
        print(f"An error occurred while displaying tasks: {e}")


def toggle_completion_handler():
    """Handle toggling task completion status"""
    try:
        task_list = get_all_tasks()
        if not task_list:
            print("No tasks available.")
            return

        display_tasks(task_list)
        task_id = get_positive_int_input("Enter the ID of the task to toggle: ")

        # Verify the task exists
        task = next((task for task in task_list if task['id'] == task_id), None)
        if not task:
            print(f"No task found with ID {task_id}.")
            return

        if toggle_task_completion(task_id):
            status = "completed" if task.get('completed', False) else "incomplete"
            print(f"Task with ID {task_id} marked as {status}!")
        else:
            print(f"Failed to toggle completion status for task with ID {task_id}.")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()