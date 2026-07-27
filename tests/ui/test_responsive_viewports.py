import pytest
from playwright.sync_api import Page, expect
from config.config import Config

@pytest.mark.ui
def test_mobile_responsive_viewport(page: Page):
    """Test web application on Mobile Viewport (iPhone 13 dimensions)."""
    # Set Mobile Viewport (390 x 844)
    page.set_viewport_size({"width": 390, "height": 844})
    page.goto(Config.BASE_URL, wait_until="domcontentloaded")
    
    # Assert body is visible on mobile
    assert page.is_visible("body"), "Body not visible on mobile viewport!"
    print("\n✅ Mobile Viewport (390x844) Responsive Test Passed!")

@pytest.mark.ui
def test_tablet_responsive_viewport(page: Page):
    """Test web application on Tablet Viewport (iPad dimensions)."""
    # Set Tablet Viewport (810 x 1080)
    page.set_viewport_size({"width": 810, "height": 1080})
    page.goto(Config.BASE_URL, wait_until="domcontentloaded")
    
    # Assert page load on tablet
    assert page.is_visible("body"), "Body not visible on tablet viewport!"
    print("✅ Tablet Viewport (810x1080) Responsive Test Passed!")
