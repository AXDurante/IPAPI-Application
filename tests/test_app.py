import pytest
from app import app  # Make sure you import the app correctly

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_home(client):
    """Test the home route"""
    response = client.get('/')
    
    # Ensure the status code is 302 (Redirect)
    assert response.status_code == 302
    
    # Check if the redirect URL is correct (to /get_ip_info)
    assert response.location == 'http://localhost/get_ip_info'

def test_get_ip_info(client):
    """Test the /get_ip_info route"""
    response = client.get('/get_ip_info')

    # Ensure the status code is 200 OK
    assert response.status_code == 200

    # Check if the response contains IP information (or an error message)
    assert b"ip" in response.data or b"Could not retrieve IP information." in response.data
