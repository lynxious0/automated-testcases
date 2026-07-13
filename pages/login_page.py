from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    URL = "https://www.saucedemo.com/"
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_CONTAINER = (By.CSS_SELECTOR, "[data-test='error']")
    ERROR_CLOSE_BUTTON = (By.CLASS_NAME, "error-button")

    def load(self):
        self.load_url(self.URL)
        return self

    def login(self, username, password):
        self.type_text(self.USERNAME_INPUT, username)
        self.type_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def is_username_enabled(self):
        return self.find(self.USERNAME_INPUT).is_enabled()

    def is_password_enabled(self):
        return self.find(self.PASSWORD_INPUT).is_enabled()

    def is_login_button_enabled(self):
        return self.find(self.LOGIN_BUTTON).is_enabled()

    def get_password_field_type(self):
        return self.find(self.PASSWORD_INPUT).get_attribute("type")

    def is_error_displayed(self):
        return self.is_visible(self.ERROR_CONTAINER)

    def get_error_text(self):
        return self.get_text(self.ERROR_CONTAINER)

    def close_error(self):
        self.click(self.ERROR_CLOSE_BUTTON)