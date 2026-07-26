from playwright.sync_api import Page, expect

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, path: str = ""):
        from config.config import Config
        url = f"{Config.BASE_URL}{path}"
        self.page.goto(url, wait_until="domcontentloaded")

    def get_title(self) -> str:
        return self.page.title()

    def click_element(self, selector: str):
        self.page.wait_for_selector(selector, state="visible")
        self.page.click(selector)

    def fill_input(self, selector: str, value: str):
        self.page.wait_for_selector(selector, state="visible")
        self.page.fill(selector, value)

    def get_text(self, selector: str) -> str:
        return self.page.inner_text(selector)
