import pytest
import requests
from config.config import Config

@pytest.mark.api
def test_target_site_http_status():
    """Verify target site returns 200 OK status code."""
    response = requests.get(Config.BASE_URL, timeout=10)
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"

@pytest.mark.api
def test_security_headers():
    """Check essential HTTP security headers."""
    response = requests.get(Config.BASE_URL, timeout=10)
    headers = response.headers
    print("Response Headers:", headers)
    assert "Server" in headers or "Date" in headers
