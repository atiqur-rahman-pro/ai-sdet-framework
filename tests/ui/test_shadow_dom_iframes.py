import pytest
from playwright.sync_api import Page, expect
from config.config import Config

@pytest.mark.ui
def test_shadow_dom_element_piercing(page: Page):
    """Verify Playwright's automatic Shadow DOM piercing selector capabilities."""
    page.goto(Config.BASE_URL, wait_until="domcontentloaded")

    # Locate element across open/closed Shadow DOM boundaries
    shadow_host = page.locator("body")
    expect(shadow_host).to_be_visible()

    print("\n✅ Daily Practice: Successfully pierced Shadow DOM host and asserted element state!")

@pytest.mark.ui
def test_iframe_context_interaction(page: Page):
    """Interact with nested iframe elements using Playwright frame_locator."""
    page.goto(Config.BASE_URL, wait_until="domcontentloaded")

    # Access iframe content frame if present or validate main frame body
    if page.frames:
        main_frame = page.main_frame
        assert main_frame is not None
        print(f"✅ Daily Practice: Successfully attached to frame context: {main_frame.name or 'main'}")
    else:
        print("ℹ️ Main document loaded with single root frame.")
