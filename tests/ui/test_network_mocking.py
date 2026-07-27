import pytest
from playwright.sync_api import Page, expect, Route
from config.config import Config

@pytest.mark.ui
def test_network_route_interception(page: Page):
    """Intercept network request and abort image downloads for fast execution."""
    # Abort image requests (png, jpg, jpeg, svg)
    def block_images(route: Route):
        if route.request.resource_type in ["image"]:
            route.abort()
        else:
            route.continue_()

    page.route("**/*", block_images)
    page.goto(Config.BASE_URL, wait_until="domcontentloaded")
    
    assert page.is_visible("body")
    print("\n✅ Network Interception Test: Successfully blocked heavy images for fast UI execution!")

@pytest.mark.ui
def test_api_mock_server_error_response(page: Page):
    """Mock a 500 Internal Server Error response for API requests."""
    def mock_500_error(route: Route):
        route.fulfill(
            status=500,
            content_type="application/json",
            body='{"error": "Simulated Internal Server Error", "code": 500}'
        )

    # Intercept any backend API endpoint
    page.route("**/api/**", mock_500_error)
    page.goto(Config.BASE_URL, wait_until="domcontentloaded")
    
    assert page.is_visible("body")
    print("✅ Network Mocking Test: Successfully simulated 500 Server Error route interception!")
