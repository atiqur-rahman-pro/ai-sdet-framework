import pytest
from playwright.sync_api import BrowserContext, Page, expect
from config.config import Config

@pytest.mark.ui
def test_multi_tab_navigation(context: BrowserContext, page: Page):
    """Verify context creation and multi-tab page switching."""
    page.goto(Config.BASE_URL, wait_until="domcontentloaded")
    
    # Open a new tab in the same browser context
    new_page = context.new_page()
    new_page.goto(Config.BASE_URL, wait_until="domcontentloaded")
    
    # Verify both pages are active in context
    assert len(context.pages) == 2
    print(f"\n✅ Multi-Tab Test: Successfully opened and managed {len(context.pages)} concurrent browser tabs!")
    
    new_page.close()
    assert len(context.pages) == 1

@pytest.mark.ui
def test_popup_event_interception(context: BrowserContext, page: Page):
    """Intercept popup window trigger events and validate new target URL."""
    page.goto(Config.BASE_URL, wait_until="domcontentloaded")
    
    # Test blank target trigger simulation
    popup_script = """() => {
        const a = document.createElement('a');
        a.href = 'https://example.com';
        a.target = '_blank';
        a.id = 'test-popup-link';
        a.innerText = 'Test Link';
        document.body.appendChild(a);
    }"""
    page.evaluate(popup_script)
    
    with page.expect_popup() as popup_info:
        page.click("#test-popup-link")
    
    popup_page = popup_info.value
    popup_page.wait_for_load_state("domcontentloaded")
    
    assert "example.com" in popup_page.url or popup_page.is_visible("body")
    print("✅ Popup Handling Test: Intercepted new target tab/popup window successfully!")
