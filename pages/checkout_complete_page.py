from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CheckoutCompletePage(BasePage):
    URL = "https://www.saucedemo.com/checkout-complete.html"

    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")
    COMPLETE_TEXT = (By.CLASS_NAME, "complete-text")
    BACK_HOME_BUTTON = (By.ID, "back-to-products")

    def is_loaded(self):
        return "checkout-complete.html" in self.current_url()

    def get_header_text(self):
        return self.get_text(self.COMPLETE_HEADER)

    def get_complete_text(self):
        return self.get_text(self.COMPLETE_TEXT)

    def back_home(self):
        self.click(self.BACK_HOME_BUTTON)
        return self