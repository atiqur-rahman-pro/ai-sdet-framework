import os
import pytest
from playwright.sync_api import Page, expect
from config.config import Config

@pytest.mark.ui
def test_full_page_screenshot_capture(page: Page):
    """Capture full-page screenshot for visual audit during execution."""
    page.goto(Config.BASE_URL, wait_until="domcontentloaded")
    
    # Create screenshots directory
    screenshots_dir = os.path.join(os.getcwd(), "screenshots")
    os.makedirs(screenshots_dir, exist_ok=True)
    screenshot_path = os.path.join(screenshots_dir, "homepage_visual_check.png")
    
    # Take full-page screenshot
    page.screenshot(path=screenshot_path, full_page=True)
    assert os.path.exists(screenshot_path)
    print(f"\n✅ Full-Page Visual Screenshot captured at: {screenshot_path}")

@pytest.mark.ui
def test_element_bounding_box_visual(page: Page):
    """Verify primary CTA element bounding box and visibility."""
    page.goto(Config.BASE_URL, wait_until="domcontentloaded")
    
    header_element = page.locator("h1, h2").first
    expect(header_element).to_be_visible()
    
    box = header_element.bounding_box()
    assert box is not None and box['width'] > 0 and box['height'] > 0
    print(f"✅ Element Visual Bounding Box verified: Width={box['width']}px, Height={box['height']}px")
