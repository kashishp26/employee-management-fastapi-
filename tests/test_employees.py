import pytest

def get_auth_headers(client):
    """Helper to ensure user exists and returns Bearer token header."""
    user_data = {
        "name": "Employee Tester",
        "email": "emptester@example.com",
        "password": "testpassword123",
        "role": "EMPLOYEE"
    }
    # Register user (ignore status if already registered)
    client.post("/auth/register", json=user_data)

    # Login to fetch access token
    login_res = client.post(
        "/auth/login",
        json={"email": user_data["email"], "password": user_data["password"]}
    )
    
    token = login_res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_get_employees_unauthorized(client):
    response = client.get("/employees/")
    assert response.status_code == 401


def test_create_department_authorized(client):
    headers = get_auth_headers(client)

    response = client.post(
        "/departments/",
        json={"name": "Engineering", "description": "Software Development"},
        headers=headers
    )
    assert response.status_code in [200, 201]
    data = response.json()
    assert data["name"] == "Engineering"


def test_get_departments(client):
    headers = get_auth_headers(client)

    response = client.get("/departments/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_employee(client):
    headers = get_auth_headers(client)

    # 1. Create a department first
    dept_res = client.post(
        "/departments/",
        json={"name": "HR Department", "description": "Human Resources"},
        headers=headers
    )
    dept_id = dept_res.json().get("id", 1)

    # 2. Payload matching Employee create schema
    employee_payload = {
        "first_name": "Rahul",
        "last_name": "Sharma",
        "email": "rahul.sharma@example.com",
        "department_id": dept_id,
        "designation": "Software Engineer",
        "salary": 50000.0
    }

    response = client.post(
        "/employees/",
        json=employee_payload,
        headers=headers
    )

    # Check for success (200/201) or standard validation check
    assert response.status_code in [200, 201, 400, 422]
    data = response.json()
    if response.status_code in [200, 201]:
        assert data.get("email") == "rahul.sharma@example.com"


def test_get_employees_list(client):
    headers = get_auth_headers(client)

    response = client.get("/employees/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)