from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CheckoutStepOnePage(BasePage):
    URL = "https://www.saucedemo.com/checkout-step-one.html"

    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    CANCEL_BUTTON = (By.ID, "cancel")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    def is_loaded(self):
        return "checkout-step-one.html" in self.current_url()

    def fill_info(self, first_name, last_name, postal_code):
        self.type_text(self.FIRST_NAME_INPUT, first_name)
        self.type_text(self.LAST_NAME_INPUT, last_name)
        self.type_text(self.POSTAL_CODE_INPUT, postal_code)
        return self

    def continue_checkout(self):
        self.click(self.CONTINUE_BUTTON)
        return self

    def cancel(self):
        self.click(self.CANCEL_BUTTON)
        return self

    def get_error_text(self):
        return self.get_text(self.ERROR_MESSAGE)

    def is_error_displayed(self):
        return self.is_visible(self.ERROR_MESSAGE)