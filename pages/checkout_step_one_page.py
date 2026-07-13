import time
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CheckoutStepOnePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.FIRST_NAME_FIELD = (By.ID, "first-name")
        self.LAST_NAME_FIELD = (By.ID, "last-name")
        self.POSTAL_CODE_FIELD = (By.ID, "postal-code")
        self.CONTINUE_BUTTON = (By.ID, "continue")
        self.CANCEL_BUTTON = (By.ID, "cancel")
        self.ERROR_CONTAINER = (By.CSS_SELECTOR, ".error-message-container")

    def enter_first_name(self, first_name):
        time.sleep(0.2)
        if first_name:
            self.type_text(self.FIRST_NAME_FIELD, first_name)

    def enter_last_name(self, last_name):
        if last_name:
            self.type_text(self.LAST_NAME_FIELD, last_name)

    def enter_postal_code(self, postal_code):
        if postal_code:
            self.type_text(self.POSTAL_CODE_FIELD, postal_code)

    def click_continue(self):
        element = self.find(self.CONTINUE_BUTTON)
        self.driver.execute_script("arguments[0].click();", element)
        time.sleep(1)

    def continue_checkout(self):
        self.click_continue()

    def fill_info(self, first_name, last_name, postal_code):
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.enter_postal_code(postal_code)

    def cancel(self):
        element = self.find(self.CANCEL_BUTTON)
        self.driver.execute_script("arguments[0].click();", element)
        time.sleep(0.5)

    def is_error_displayed(self):
        try:
            return self.is_visible(self.ERROR_CONTAINER)
        except Exception:
            return False

    def get_error_text(self):
        return self.get_text(self.ERROR_CONTAINER)