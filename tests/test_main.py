import os
import pytest
import requests_mock
from unittest.mock import patch
from flask import Flask
from flask.testing import FlaskClient

# Import the app instance AFTER potentially patching environment variables
# or setting up mocks if needed globally, but here we do it per test/fixture.
# from app.main import app as flask_app # Renamed to avoid conflict

# It's often better practice to create the app within a fixture
# to ensure isolation and allow configuration changes per test suite.
from app.main import app as flask_app, limiter

@pytest.fixture(scope='module')
def app() -> Flask:
    """Create and configure a new app instance for each test module."""
    # Configure the app for testing
    flask_app.config.update({
        "TESTING": True,
        # Disable CSRF protection in tests if you have it enabled
        # "WTF_CSRF_ENABLED": False,
        # Use a different limiter storage for tests if needed, memory is usually fine
        "RATELIMIT_STORAGE_URI": "memory://",
    })
    # Reset limiter state before tests if necessary
    limiter.reset()
    yield flask_app

@pytest.fixture()
def client(app: Flask) -> FlaskClient:
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def mock_env():
    """Fixture to mock environment variables."""
    with patch.dict(os.environ, {"API_KEY": "test-api-key"}):
        yield

# --- Test Cases ---

def test_hello_route(client: FlaskClient):
    """Test the '/' route."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json == {"message": "Hello World"}
    # Check for security headers (basic check)
    assert 'Content-Security-Policy' in response.headers

def test_health_route_success(client: FlaskClient):
    """Test the '/health' route succeeds within limits."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json == {"status": "healthy"}

def test_health_route_rate_limit(client: FlaskClient):
    """Test the '/health' route rate limiting."""
    # Hit the endpoint just enough times to exceed the limit (5 per minute)
    for _ in range(5):
        response = client.get("/health")
        assert response.status_code == 200

    # The 6th request should be rate limited
    response = client.get("/health")
    assert response.status_code == 429
    assert "Rate limit exceeded" in response.json["error"]

@requests_mock.Mocker(kw='mock')
def test_random_name_route_success(client: FlaskClient, mock_env, **kwargs):
    """Test the '/random-name' route successfully fetches and sanitizes."""
    mock = kwargs['mock']
    mock_url = "https://randommer.io/api/Name"
    mock_name = "Test Name <script>alert('xss')</script>"
    sanitized_name = "Test Name alert('xss')" # How bleach cleans this specific case

    mock.get(mock_url, text=mock_name)

    response = client.get("/random-name")

    assert response.status_code == 200
    assert response.json == {"name": sanitized_name}
    assert mock.called_once
    assert mock.last_request.headers['X-Api-Key'] == 'test-api-key'

@requests_mock.Mocker(kw='mock')
def test_random_name_route_api_failure(client: FlaskClient, mock_env, **kwargs):
    """Test the '/random-name' route handles API failure."""
    mock = kwargs['mock']
    mock_url = "https://randommer.io/api/Name"
    mock.get(mock_url, status_code=500, text="API Error")

    response = client.get("/random-name")

    assert response.status_code == 500
    assert response.json == {"error": "Failed to fetch random name"}
    assert mock.called_once

def test_random_name_route_missing_api_key(client: FlaskClient):
    """Test '/random-name' without API_KEY (relies on startup validation)."""
    # Note: This test assumes validate_secrets() would prevent the app from
    # starting properly if the key is missing. Testing that requires
    # more complex setup (e.g., running the app creation in a subprocess
    # or mocking sys.exit/print).
    # For a unit/integration test like this, we often assume the key
    # *would* be present due to validation, or mock it like in mock_env.
    # If we wanted to test the *absence* after startup (e.g., if validation failed
    # silently), we'd need to explicitly unset the mocked env var.
    with patch.dict(os.environ, clear=True): # Ensure API_KEY is not set
        # We expect the API call to fail because the key is missing in the request logic
        # (even if validate_secrets was somehow bypassed or didn't exit)
        # The current code fetches os.getenv("API_KEY") inside the route.
        # If it's None, the api.GET_page might fail or behave unexpectedly.
        # Let's assume api.GET_page handles a missing key gracefully or raises error.
        # For this test, let's mock GET_page to see if the route handles its absence.

        # Patch the function that uses the key
        with patch('app.modules.api.GET_page', side_effect=Exception("Simulated API call failure")):
             response = client.get("/random-name")
             # Expecting a 500 error because the API call failed
             assert response.status_code == 500
             assert response.json == {"error": "Failed to fetch random name"}

# It might be useful to test validate_secrets directly, though it involves mocking os.getenv and print/exit
def test_validate_secrets_success(capsys):
    """Test validate_secrets succeeds when key is present."""
    from app.main import validate_secrets
    with patch.dict(os.environ, {"API_KEY": "test-key"}):
        validate_secrets()
    captured = capsys.readouterr()
    assert "Secrets validated successfully." in captured.out
    assert "Error" not in captured.out

def test_validate_secrets_failure(capsys):
    """Test validate_secrets fails and prints error when key is missing."""
    from app.main import validate_secrets
    with patch.dict(os.environ, clear=True): # Ensure API_KEY is not set
        with pytest.raises(SystemExit) as pytest_wrapped_e:
             validate_secrets()
    captured = capsys.readouterr()
    assert "Error: API_KEY environment variable not set." in captured.out
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1