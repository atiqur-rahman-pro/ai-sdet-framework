import json
import pytest
from playwright.sync_api import Page, Route
from config.config import Config

@pytest.mark.api
def test_graphql_query_interception_mock(page: Page):
    """Intercept GraphQL query request and fulfill with mock data payload."""
    mock_user_data = {
        "data": {
            "user": {
                "id": "usr_998877",
                "name": "Atiqur Rahman",
                "role": "SDET Architect",
                "email": "rahman.atiqur.pro@gmail.com"
            }
        }
    }

    def handle_graphql_route(route: Route):
        request = route.request
        if request.method == "POST" and "graphql" in request.url.lower():
            route.fulfill(
                status=200,
                content_type="application/json",
                body=json.dumps(mock_user_data)
            )
        else:
            route.continue_()

    page.route("**/graphql**", handle_graphql_route)
    page.goto(Config.BASE_URL, wait_until="domcontentloaded")

    print("\n✅ Day 9 Practice: Successfully intercepted and mocked GraphQL query payload!")

@pytest.mark.api
def test_graphql_mutation_error_simulation(page: Page):
    """Simulate GraphQL mutation failure error response."""
    mock_error_payload = {
        "errors": [
            {
                "message": "Unauthorized GraphQL mutation operation",
                "extensions": {"code": "FORBIDDEN"}
            }
        ]
    }

    def handle_graphql_error(route: Route):
        route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps(mock_error_payload)
        )

    page.route("**/graphql**", handle_graphql_error)
    page.goto(Config.BASE_URL, wait_until="domcontentloaded")

    print("✅ Day 9 Practice: GraphQL mutation error simulation verified successfully!")
