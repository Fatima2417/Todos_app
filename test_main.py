"""
Test script for Todo In-Memory Python Console App
Validates all functionality works correctly
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import main application functions from main.py
import main

def test_add_task():
    """Test adding a task"""
    print("Testing add_task function...")
    main.reset_storage()  # Reset storage before test

    # Add a task
    task = main.add_task("Test Task", "Test Description")

    # Verify task was added
    assert task["id"] == 1, f"Expected ID 1, got {task['id']}"
    assert task["title"] == "Test Task", f"Expected title 'Test Task', got {task['title']}"
    assert task["description"] == "Test Description", f"Expected description 'Test Description', got {task['description']}"
    assert task["completed"] == False, f"Expected completed False, got {task['completed']}"

    print("OK add_task function works correctly")
    return True


def test_get_all_tasks():
    """Test getting all tasks"""
    print("Testing get_all_tasks function...")
    main.reset_storage()  # Reset storage before test

    # Add a task
    main.add_task("Test Task", "Test Description")

    # Get all tasks
    tasks = main.get_all_tasks()

    # Verify we got the task back
    assert len(tasks) == 1, f"Expected 1 task, got {len(tasks)}"
    assert tasks[0]["id"] == 1, f"Expected ID 1, got {tasks[0]['id']}"
    assert tasks[0]["title"] == "Test Task", f"Expected title 'Test Task', got {tasks[0]['title']}"

    print("OK get_all_tasks function works correctly")
    return True


def test_update_task():
    """Test updating a task"""
    print("Testing update_task function...")
    main.reset_storage()  # Reset storage before test

    # Add a task
    main.add_task("Original Title", "Original Description")

    # Update the task
    success = main.update_task(1, "Updated Title", "Updated Description")

    # Verify update was successful
    assert success == True, f"Expected update to succeed, got {success}"

    # Get the updated task
    tasks = main.get_all_tasks()
    updated_task = tasks[0]

    assert updated_task["title"] == "Updated Title", f"Expected title 'Updated Title', got {updated_task['title']}"
    assert updated_task["description"] == "Updated Description", f"Expected description 'Updated Description', got {updated_task['description']}"

    print("OK update_task function works correctly")
    return True


def test_delete_task():
    """Test deleting a task"""
    print("Testing delete_task function...")
    main.reset_storage()  # Reset storage before test

    # Add two tasks
    main.add_task("Task 1", "Description 1")
    main.add_task("Task 2", "Description 2")

    # Verify both tasks exist
    tasks = main.get_all_tasks()
    assert len(tasks) == 2, f"Expected 2 tasks before deletion, got {len(tasks)}"

    # Delete one task
    success = main.delete_task(1)

    # Verify deletion was successful
    assert success == True, f"Expected deletion to succeed, got {success}"

    # Verify only one task remains
    tasks = main.get_all_tasks()
    assert len(tasks) == 1, f"Expected 1 task after deletion, got {len(tasks)}"
    assert tasks[0]["id"] == 2, f"Expected remaining task ID to be 2, got {tasks[0]['id']}"

    print("OK delete_task function works correctly")
    return True


def test_toggle_completion():
    """Test toggling task completion"""
    print("Testing toggle_task_completion function...")
    main.reset_storage()  # Reset storage before test

    # Add a task
    main.add_task("Test Task", "Test Description")

    # Verify initial state is incomplete
    tasks = main.get_all_tasks()
    assert tasks[0]["completed"] == False, f"Expected task to be incomplete initially, got {tasks[0]['completed']}"

    # Toggle completion
    success = main.toggle_task_completion(1)

    # Verify toggle was successful
    assert success == True, f"Expected toggle to succeed, got {success}"

    # Verify task is now complete
    tasks = main.get_all_tasks()
    assert tasks[0]["completed"] == True, f"Expected task to be complete after toggle, got {tasks[0]['completed']}"

    # Toggle again
    success = main.toggle_task_completion(1)
    assert success == True, f"Expected second toggle to succeed, got {success}"

    # Verify task is now incomplete again
    tasks = main.get_all_tasks()
    assert tasks[0]["completed"] == False, f"Expected task to be incomplete after second toggle, got {tasks[0]['completed']}"

    print("OK toggle_task_completion function works correctly")
    return True


def run_tests():
    """Run all tests"""
    print("Starting tests for Todo In-Memory Python Console App...\n")

    tests = [
        test_add_task,
        test_get_all_tasks,
        test_update_task,
        test_delete_task,
        test_toggle_completion
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        try:
            result = test()
            if result:
                passed += 1
            print()  # Add blank line between tests
        except Exception as e:
            print(f"FAILED: {test.__name__} failed with error: {e}\n")

    print(f"Tests completed: {passed}/{total} passed")

    if passed == total:
        print("SUCCESS: All tests passed! The application is working correctly.")
        return True
    else:
        print("FAILURE: Some tests failed.")
        return False


if __name__ == "__main__":
    run_tests()