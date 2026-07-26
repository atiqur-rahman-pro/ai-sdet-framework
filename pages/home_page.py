from pages.base_page import BasePage

class HomePage(BasePage):
    # Selectors
    HEADER_TITLE = "h1, h2"
    BOOK_CONSULTATION_BTN = 'a[href*="assessment"], a[href*="contact"]'
    NAV_ABOUT = 'a[href*="about-us"]'
    NAV_SERVICES = 'a[href*="services"]'
    NAV_CONTACT = 'a[href*="contact"]'

    def open_home(self):
        self.navigate("/")

    def click_about_us(self):
        self.click_element(self.NAV_ABOUT)

    def click_services(self):
        self.click_element(self.NAV_SERVICES)

    def click_contact(self):
        self.click_element(self.NAV_CONTACT)
