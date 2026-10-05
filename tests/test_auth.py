def test_register_user(client):
    response = client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": "testuser@example.com",
            "password": "testpassword123",
            "role": "EMPLOYEE"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "testuser@example.com"
    assert "id" in data

def test_login_user(client):
    response = client.post(
        "/auth/login",
        json={
            "email": "testuser@example.com",
            "password": "testpassword123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials(client):
    response = client.post(
        "/auth/login",
        json={
            "email": "testuser@example.com",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401

def test_register_duplicate_email(client):
    
    response = client.post(
        "/auth/register",
        json={
            "name": "Duplicate User",
            "email": "testuser@example.com",
            "password": "anotherpassword123",
            "role": "EMPLOYEE"
        }
    )
    assert response.status_code in [400, 409]