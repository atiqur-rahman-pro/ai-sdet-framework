from pages.base_page import BasePage

class AssessmentPage(BasePage):
    # Selectors
    PAGE_HEADING = "h1, h2"
    FORM = "form"
    SUBMIT_BTN = 'button[type="submit"], input[type="submit"]'

    def open_assessment(self):
        self.navigate("/sleep-apnea-assessment")

    def is_form_present(self) -> bool:
        return self.page.locator(self.FORM).count() > 0 or self.page.locator(self.PAGE_HEADING).count() > 0
