def test_get_employees_unauthorized(client):
    response = client.get("/employees/")
    assert response.status_code == 401