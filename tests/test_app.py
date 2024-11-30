import pytest
from app import app  # Replace 'app' with your Flask application file name

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_ip_info(client):
    response = client.get('/get_ip_info')
    assert response.status_code == 200
    assert b"Public IP Information" in response.data  # Ensure the page contains expected text
