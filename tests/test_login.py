import unittest
from selenium import webdriver
from pages.login_page import LoginPage
from tests import config


class LoginTests(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.login_page = LoginPage(self.driver)
        self.login_page.load()

    def tearDown(self):
        self.driver.quit()

    def test_login_fields_are_enabled_and_masked(self):
        self.assertTrue(self.login_page.is_username_enabled())
        self.assertTrue(self.login_page.is_password_enabled())
        self.assertEqual(self.login_page.get_password_field_type(), "password")

    def test_login_button_is_enabled(self):
        self.assertTrue(self.login_page.is_login_button_enabled())

    def test_valid_login_standard_user(self):
        self.login_page.login(config.STANDARD_USER, config.PASSWORD)
        self.assertIn("inventory.html", self.driver.current_url)

    def test_login_problem_user(self):
        self.login_page.login(config.PROBLEM_USER, config.PASSWORD)
        self.assertIn("inventory.html", self.driver.current_url)

    def test_login_performance_glitch_user(self):
        self.login_page.login(config.PERFORMANCE_GLITCH_USER, config.PASSWORD)
        self.assertIn("inventory.html", self.driver.current_url)

    def test_login_error_user(self):
        self.login_page.login(config.ERROR_USER, config.PASSWORD)
        self.assertIn("inventory.html", self.driver.current_url)

    def test_login_visual_user(self):
        self.login_page.login(config.VISUAL_USER, config.PASSWORD)
        self.assertIn("inventory.html", self.driver.current_url)

    def test_locked_out_user_shows_error(self):
        self.login_page.login(config.LOCKED_OUT_USER, config.PASSWORD)
        self.assertTrue(self.login_page.is_error_displayed())
        self.assertIn("locked out", self.login_page.get_error_text().lower())

    def test_invalid_password_shows_error(self):
        self.login_page.login(config.STANDARD_USER, "wrong_password")
        self.assertTrue(self.login_page.is_error_displayed())
        self.assertIn("do not match", self.login_page.get_error_text().lower())

    def test_unregistered_username_shows_error(self):
        self.login_page.login("no_such_user", config.PASSWORD)
        self.assertTrue(self.login_page.is_error_displayed())
        self.assertIn("do not match", self.login_page.get_error_text().lower())

    def test_empty_username_shows_error(self):
        self.login_page.login("", config.PASSWORD)
        self.assertTrue(self.login_page.is_error_displayed())
        self.assertIn("username is required", self.login_page.get_error_text().lower())

    def test_empty_password_shows_error(self):
        self.login_page.login(config.STANDARD_USER, "")
        self.assertTrue(self.login_page.is_error_displayed())
        self.assertIn("password is required", self.login_page.get_error_text().lower())

    def test_empty_fields_shows_error(self):
        self.login_page.login("", "")
        self.assertTrue(self.login_page.is_error_displayed())
        self.assertIn("username is required", self.login_page.get_error_text().lower())

    def test_error_message_can_be_closed(self):
        self.login_page.login("", "")
        self.assertTrue(self.login_page.is_error_displayed())
        self.login_page.close_error()
        self.assertFalse(self.login_page.is_error_displayed())


if __name__ == "__main__":
    unittest.main()