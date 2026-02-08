import requests
import random
import json

BASE_URL = "http://localhost:8000"

def test_toggle_completion():
    # 1. Signup/Login to get a fresh user
    email = f"toggle_test_{random.randint(1000, 9999)}@example.com"
    password = "password123"
    print(f"Creating test user: {email}")
    
    resp = requests.post(f"{BASE_URL}/auth/sign-up/email", json={"email": email, "password": password})
    if resp.status_code != 200:
        print(f"Signup failed: {resp.status_code} {resp.text}")
        return
    
    auth_data = resp.json()
    user_id = auth_data["user"]["id"]
    token = auth_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print(f"User ID: {user_id}")

    # 2. Create a task
    create_response = requests.post(
        f"{BASE_URL}/api/v1/{user_id}/tasks",
        headers=headers,
        json={"title": "Test toggle task", "description": "Test description"}
    )
    
    task = create_response.json()
    task_id = task["id"]
    print(f"Created task {task_id}, initial completed: {task['completed']}")
    
    # 3. First Toggle (should become True)
    print("Toggling completion (1st time)...")
    toggle_response = requests.patch(
        f"{BASE_URL}/api/v1/{user_id}/tasks/{task_id}/complete",
        headers=headers
    )
    if toggle_response.status_code == 200:
        print(f"After first toggle: {toggle_response.json()['completed']}")
    else:
        print(f"First toggle failed: {toggle_response.status_code} {toggle_response.text}")
    
    # 4. Second Toggle (should become False)
    print("Toggling completion (2nd time)...")
    toggle_response2 = requests.patch(
        f"{BASE_URL}/api/v1/{user_id}/tasks/{task_id}/complete",
        headers=headers
    )
    if toggle_response2.status_code == 200:
        print(f"After second toggle: {toggle_response2.json()['completed']}")
    else:
        print(f"Second toggle failed: {toggle_response2.status_code} {toggle_response2.text}")

if __name__ == "__main__":
    test_toggle_completion()
