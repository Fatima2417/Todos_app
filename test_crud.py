import requests
import random
import uuid

BASE_URL = "http://localhost:8000"

def test_crud():
    # 1. Signup/Login
    email = f"crud_test_{random.randint(1000, 9999)}@example.com"
    password = "password123"
    print(f"Testing with email: {email}")
    
    resp = requests.post(f"{BASE_URL}/auth/sign-up/email", json={"email": email, "password": password})
    if resp.status_code != 200:
        print(f"Signup failed: {resp.status_code} {resp.text}")
        return
    
    auth_data = resp.json()
    user_id = auth_data["user"]["id"]
    token = auth_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print(f"User created: {user_id}")

    # 2. CREATE Task
    task_data = {"title": "Test Task", "description": "CRUD test description"}
    resp = requests.post(f"{BASE_URL}/api/v1/{user_id}/tasks", json=task_data, headers=headers)
    if resp.status_code != 201:
        print(f"Create task failed: {resp.status_code} {resp.text}")
        return
    
    task = resp.json()
    task_id = task["id"]
    print(f"Task created: {task_id}")

    # 3. READ Tasks
    resp = requests.get(f"{BASE_URL}/api/v1/{user_id}/tasks", headers=headers)
    if resp.status_code != 200:
        print(f"Read tasks failed: {resp.status_code} {resp.text}")
        return
    
    tasks = resp.json()
    print(f"Tasks count: {len(tasks)}")
    assert any(t["id"] == task_id for t in tasks)

    # 4. UPDATE Task
    update_data = {"title": "Updated Task Title", "description": "Updated description"}
    resp = requests.put(f"{BASE_URL}/api/v1/{user_id}/tasks/{task_id}", json=update_data, headers=headers)
    if resp.status_code != 200:
        print(f"Update task failed: {resp.status_code} {resp.text}")
        return
    
    updated_task = resp.json()
    print(f"Task updated: {updated_task['title']}")
    assert updated_task["title"] == "Updated Task Title"

    # 5. TOGGLE Completion
    resp = requests.patch(f"{BASE_URL}/api/v1/{user_id}/tasks/{task_id}/complete", headers=headers)
    if resp.status_code != 200:
        print(f"Toggle completion failed: {resp.status_code} {resp.text}")
        return
    
    toggled_task = resp.json()
    print(f"Task completed: {toggled_task['completed']}")
    assert toggled_task["completed"] is True

    # 6. DELETE Task
    resp = requests.delete(f"{BASE_URL}/api/v1/{user_id}/tasks/{task_id}", headers=headers)
    if resp.status_code != 204:
        print(f"Delete task failed: {resp.status_code} {resp.text}")
        return
    
    print("Task deleted successfully")

    # Verify deletion
    resp = requests.get(f"{BASE_URL}/api/v1/{user_id}/tasks", headers=headers)
    tasks = resp.json()
    assert all(t["id"] != task_id for t in tasks)
    print("CRUD test passed successfully!")

if __name__ == "__main__":
    test_crud()
