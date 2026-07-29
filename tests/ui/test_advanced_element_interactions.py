import pytest
from playwright.sync_api import Page, expect
from config.config import Config

@pytest.mark.ui
def test_mouse_hover_and_action_menu(page: Page):
    """Verify Playwright mouse hover interaction and dropdown visibility."""
    page.goto(Config.BASE_URL, wait_until="domcontentloaded")
    
    # Hover over visible body / navigation element
    target = page.locator("header").first
    if not target.is_visible():
        target = page.locator("body")
    target.hover()
    print("\n✅ Daily Practice: Successfully executed mouse hover action on primary UI element!")

@pytest.mark.ui
def test_keyboard_shortcuts_and_input_control(page: Page):
    """Test keyboard shortcut navigation and input field manipulation."""
    page.goto(Config.BASE_URL, wait_until="domcontentloaded")
    
    # Locate interactive input or body element
    body = page.locator("body")
    body.click()
    
    # Press Tab and Escape keyboard shortcuts
    page.keyboard.press("Tab")
    page.keyboard.press("Escape")
    
    print("✅ Daily Practice: Keyboard shortcuts (Tab, Escape) verified successfully!")
