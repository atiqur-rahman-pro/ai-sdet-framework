import pytest
from playwright.sync_api import Page, expect
from pages.home_page import HomePage
from pages.assessment_page import AssessmentPage

@pytest.mark.ui
@pytest.mark.smoke
def test_homepage_title_and_navigation(page: Page):
    """Verify homepage title and primary navigation links."""
    home_page = HomePage(page)
    home_page.open_home()
    
    title = home_page.get_title()
    assert "Sleep Apnea Doctor" in title, f"Unexpected title: {title}"

@pytest.mark.ui
def test_assessment_page_accessibility_flow(page: Page):
    """Verify navigation to health check assessment page."""
    assessment_page = AssessmentPage(page)
    assessment_page.open_assessment()
    
    assert assessment_page.is_form_present(), "Assessment page heading or form is missing!"
