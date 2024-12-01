import pytest
from flask import template_rendered
from app import app  # Import your Flask app
from unittest.mock import patch, Mock


@pytest.fixture
def client():
    # Create a test client for the Flask app
    with app.test_client() as client:
        yield client


@pytest.fixture
def captured_templates():
    # Capture rendered templates for assertions
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, app)
    yield recorded
    template_rendered.disconnect(record, app)


def test_get_ip_info_success(client, captured_templates):
    # Mock the `requests.get` call to return sample IP data
    sample_ip_data = {
        'ip': '203.0.113.195',
        'version': 'IPv4',
        'city': 'Sample City',
        'region': 'Sample Region',
        'country_name': 'Sample Country',
        'country_code': 'SC',
        'latitude': 45.0,
        'longitude': -93.0,
        'asn': 'AS12345',
        'org': 'Sample Organization',
    }
    with patch('app.requests.get') as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = sample_ip_data
        mock_response.raise_for_status = Mock()  # Simulate no HTTP errors
        mock_get.return_value = mock_response

        response = client.get('/get_ip_info')
        assert response.status_code == 200

        # Check rendered template
        assert len(captured_templates) == 1
        template, context = captured_templates[0]
        assert template.name == 'index.html'
        assert 'ip_info' in context
        assert context['ip_info']['ip'] == '203.0.113.195'


def test_get_ip_info_error(client, captured_templates):
    # Mock the `requests.get` call to raise an exception
    with patch('app.requests.get') as mock_get:
        mock_get.side_effect = Exception('API error')

        response = client.get('/get_ip_info')
        assert response.status_code == 200

        # Check rendered template for error message
        assert len(captured_templates) == 1
        template, context = captured_templates[0]
        assert template.name == 'index.html'
        assert 'error' in context
        assert 'Service temporarily unavailable' in context['error']
