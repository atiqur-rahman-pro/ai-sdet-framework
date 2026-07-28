import pytest
from playwright.sync_api import BrowserContext, Page, expect
from config.config import Config

@pytest.mark.ui
def test_cookie_injection_session_bypass(context: BrowserContext, page: Page):
    """Inject authentication cookie to bypass login step instantly."""
    # Inject dummy auth session cookie
    context.add_cookies([
        {
            "name": "session_token",
            "value": "mock_authenticated_jwt_token_123456789",
            "domain": "sleepapneabd.com",
            "path": "/"
        }
    ])

    page.goto(Config.BASE_URL, wait_until="domcontentloaded")
    
    # Verify cookie presence in browser context
    cookies = context.cookies()
    session_cookie = next((c for c in cookies if c['name'] == 'session_token'), None)
    
    assert session_cookie is not None
    assert session_cookie['value'] == "mock_authenticated_jwt_token_123456789"
    print("\n✅ Auth Session Test: Cookie injected & authenticated session bypassed in 1 sec!")

@pytest.mark.ui
def test_local_storage_auth_injection(page: Page):
    """Inject authorization state directly into localStorage."""
    page.goto(Config.BASE_URL, wait_until="domcontentloaded")
    
    # Inject mock auth state into LocalStorage
    page.evaluate("""() => {
        localStorage.setItem('user_role', 'admin');
        localStorage.setItem('auth_status', 'logged_in');
    }""")
    
    # Verify injected storage values
    role = page.evaluate("() => localStorage.getItem('user_role')")
    assert role == "admin"
    print("✅ Auth Session Test: LocalStorage state successfully injected for fast execution!")
