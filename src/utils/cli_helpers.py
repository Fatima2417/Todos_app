"""
CLI Helpers for Todo In-Memory Python Console App
Provides utility functions for CLI input/output operations
"""


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