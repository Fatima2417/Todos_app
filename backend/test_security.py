import requests
import random

BASE_URL = "http://localhost:8000"

def test_user_isolation():
    # 1. Create User A
    print("Setting up User A...")
    resp_a = requests.post(f"{BASE_URL}/auth/sign-up/email", 
                          json={"email": f"user_a_{random.randint(1000,9999)}@test.com", "password": "password123"})
    user_a = resp_a.json()
    token_a = user_a["access_token"]
    id_a = user_a["user"]["id"]
    
    # 2. Create Task for User A
    resp_task = requests.post(f"{BASE_URL}/api/v1/{id_a}/tasks", 
                             json={"title": "Secret Task"}, 
                             headers={"Authorization": f"Bearer {token_a}"})
    task_id = resp_task.json()["id"]
    print(f"User A created task {task_id}")

    # 3. Create User B
    print("Setting up User B...")
    resp_b = requests.post(f"{BASE_URL}/auth/sign-up/email", 
                          json={"email": f"user_b_{random.randint(1000,9999)}@test.com", "password": "password123"})
    user_b = resp_b.json()
    token_b = user_b["access_token"]
    id_b = user_b["user"]["id"]

    # 4. Attempt to access User A's task using User B's token
    print(f"User B (ID: {id_b}) attempting to access User A's task...")
    resp_illegal = requests.get(f"{BASE_URL}/api/v1/{id_a}/tasks/{task_id}", 
                               headers={"Authorization": f"Bearer {token_b}"})
    
    print(f"Response code: {resp_illegal.status_code}")
    if resp_illegal.status_code == 403 or resp_illegal.status_code == 401 or resp_illegal.status_code == 404:
        print("SUCCESS: Isolation maintained (User B cannot access User A's task)")
    else:
        print(f"FAILURE: Security breach! User B accessed task. Response: {resp_illegal.text}")

if __name__ == "__main__":
    test_user_isolation()
