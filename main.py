"""
Todo In-Memory Python Console App
Complete application in a single file for easy execution
"""

# Task data model - in-memory storage
tasks = []  # List to store all tasks
next_id = 1  # Counter for the next available task ID


def add_task(title, description=""):
    """
    Add a new task to the in-memory store

    Args:
        title (str): The task title (required)
        description (str): The task description (optional)

    Returns:
        dict: The created task with id, title, description, and completed status
    """
    global next_id

    # Validate input
    if not title or not isinstance(title, str) or len(title.strip()) == 0:
        raise ValueError("Task title is required and must be a non-empty string")

    # Create the new task
    task = {
        "id": next_id,
        "title": title.strip(),
        "description": description.strip() if description else "",
        "completed": False
    }

    # Add to the tasks list
    tasks.append(task)

    # Increment the ID counter
    next_id += 1

    return task


def get_all_tasks():
    """
    Retrieve all tasks from the in-memory store

    Returns:
        list: A list of all task dictionaries
    """
    return tasks


def get_task_by_id(task_id):
    """
    Retrieve a specific task by its ID

    Args:
        task_id (int): The unique identifier of the task

    Returns:
        dict: The task dictionary if found, None otherwise
    """
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


def update_task(task_id, title=None, description=None):
    """
    Update an existing task's properties

    Args:
        task_id (int): The unique identifier of the task to update
        title (str, optional): New title if provided
        description (str, optional): New description if provided

    Returns:
        bool: True if successful, False if task not found
    """
    task = get_task_by_id(task_id)
    if not task:
        return False

    if title is not None:
        if not isinstance(title, str) or len(title.strip()) == 0:
            raise ValueError("Task title must be a non-empty string if provided")
        task["title"] = title.strip()

    if description is not None:
        task["description"] = description.strip() if description else ""

    return True


def delete_task(task_id):
    """
    Remove a task from the in-memory store by ID

    Args:
        task_id (int): The unique identifier of the task to delete

    Returns:
        bool: True if successful, False if task not found
    """
    global tasks
    initial_length = len(tasks)

    # Filter out the task with the given ID
    tasks = [task for task in tasks if task["id"] != task_id]

    # Check if any task was removed
    return len(tasks) != initial_length


def toggle_task_completion(task_id):
    """
    Toggle the completion status of a task

    Args:
        task_id (int): The unique identifier of the task to update

    Returns:
        bool: True if successful, False if task not found
    """
    task = get_task_by_id(task_id)
    if not task:
        return False

    task["completed"] = not task["completed"]
    return True


def reset_storage():
    """
    Reset the in-memory storage for testing purposes
    """
    global tasks, next_id
    tasks = []
    next_id = 1


def display_menu(options):
    """
    Display a numbered menu to the user

    Args:
        options (list): List of menu option strings
    """
    print("\n--- MENU ---")
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    print("-----------")


def display_tasks(task_list):
    """
    Display the list of tasks in a formatted way

    Args:
        task_list (list): List of task dictionaries to display
    """
    if not task_list:
        print("\nNo tasks found.")
        return

    print("\n--- TASK LIST ---")
    print(f"{'ID':<4} {'Status':<8} {'Title':<20} {'Description'}")
    print("-" * 60)

    for task in task_list:
        status = "✓" if task["completed"] else "○"
        title = task["title"][:17] + "..." if len(task["title"]) > 20 else task["title"]
        desc = task["description"][:30] + "..." if len(task["description"]) > 30 else task["description"]
        print(f"{task['id']:<4} {status:<8} {title:<20} {desc}")
    print("-" * 60)


def get_validated_input(prompt, validator_func=None, error_message="Invalid input. Please try again."):
    """
    Get validated input from the user

    Args:
        prompt (str): The input prompt to display
        validator_func (callable, optional): Function to validate the input
        error_message (str): Error message to display for invalid input

    Returns:
        The validated input value
    """
    while True:
        user_input = input(prompt)
        if validator_func:
            try:
                result = validator_func(user_input)
                if result is not None:
                    return result
                else:
                    print(error_message)
            except ValueError:
                print(error_message)
        else:
            return user_input


def get_positive_int_input(prompt, error_message="Please enter a valid positive integer."):
    """
    Get a positive integer input from the user

    Args:
        prompt (str): The input prompt to display
        error_message (str): Error message to display for invalid input

    Returns:
        int: The positive integer entered by the user
    """
    def validator(value):
        try:
            num = int(value)
            if num > 0:
                return num
        except ValueError:
            pass
        return None

    return get_validated_input(prompt, validator, error_message)


def confirm_action(message):
    """
    Ask the user to confirm an action

    Args:
        message (str): The confirmation message to display

    Returns:
        bool: True if user confirms, False otherwise
    """
    response = input(f"{message} (y/n): ").strip().lower()
    return response in ['y', 'yes', '1']


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
            status = "completed" if not task.get('completed', False) else "incomplete"
            print(f"Task with ID {task_id} marked as {status}!")
        else:
            print(f"Failed to toggle completion status for task with ID {task_id}.")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


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


if __name__ == "__main__":
    main()