from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CheckoutStepOnePage(BasePage):
    """CCF-021..029: Checkout info page.

    Note: saucedemo.com's checkout-step-one page only collects first name,
    last name, and postal code. There is no payment input field on this
    site (CCF-025 in the source doc), so no payment-related locator exists
    here on purpose.
    """

    URL = "https://www.saucedemo.com/checkout-step-one.html"
    FIRST_NAME_FIELD = (By.ID, "first-name")
    LAST_NAME_FIELD = (By.ID, "last-name")
    POSTAL_CODE_FIELD = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    CANCEL_BUTTON = (By.ID, "cancel")
    ERROR_CONTAINER = (By.CSS_SELECTOR, "[data-test='error']")

    def is_loaded(self):
        return "checkout-step-one.html" in self.current_url()

    def enter_first_name(self, first_name):
        if first_name:
            self.type_text(self.FIRST_NAME_FIELD, first_name)

    def enter_last_name(self, last_name):
        if last_name:
            self.type_text(self.LAST_NAME_FIELD, last_name)

    def enter_postal_code(self, postal_code):
        if postal_code:
            self.type_text(self.POSTAL_CODE_FIELD, postal_code)

    def fill_info(self, first_name, last_name, postal_code):
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.enter_postal_code(postal_code)

    def continue_checkout(self):
        self.click(self.CONTINUE_BUTTON)

    def cancel(self):
        self.click(self.CANCEL_BUTTON)
        self.wait_for_url_contains("cart.html")

    def is_error_displayed(self):
        return self.is_visible(self.ERROR_CONTAINER)

    def get_error_text(self):
        return self.get_text(self.ERROR_CONTAINER)
