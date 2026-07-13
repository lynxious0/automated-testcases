"""
Covers the User Login Feature (ULF-001..020) and the Global/negative
login cases (GLB-001..003) from the test case docs.

Three IDs describe UI saucedemo.com does not actually have and are
marked skip() with a reason instead of being faked:
  ULF-014 User Logout Confirmation
  ULF-015 User Logout Confirmation Confirm Button
  ULF-016 User Logout Confirmation Cancel Button
    -> Clicking Logout in the sidebar logs out immediately; there is
       no confirmation dialog on this site.
  ULF-018 Logged Out Page Inactivity
    -> saucedemo.com has no session-timeout/inactivity feature to
       exercise.
"""
import unittest
from selenium import webdriver
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from tests import config


class LoginTests(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.login_page = LoginPage(self.driver)
        self.login_page.load()

    def tearDown(self):
        self.driver.quit()

    def test_ULF_001_user_login_valid_credentials(self):
        self.login_page.login(config.STANDARD_USER, config.PASSWORD)
        self.login_page.wait_for_url_contains("inventory.html")
        self.assertIn("inventory.html", self.driver.current_url)

    def test_ULF_002_login_username_input_field(self):
        self.assertTrue(self.login_page.is_username_enabled())

    def test_ULF_003_login_password_input_field(self):
        self.assertTrue(self.login_page.is_password_enabled())

    def test_ULF_004_login_password_mask(self):
        self.assertEqual(self.login_page.get_password_field_type(), "password")

    def test_ULF_005_login_button_enabled(self):
        self.assertTrue(self.login_page.is_login_button_enabled())

    def test_ULF_006_login_button_success(self):
        self.login_page.login(config.STANDARD_USER, config.PASSWORD)
        self.login_page.wait_for_url_contains("inventory.html")
        self.assertIn("inventory.html", self.driver.current_url)

    def test_ULF_006b_login_button_success_all_working_users(self):
        # standard_user is covered above; the other 4 non-locked accounts
        # should also authenticate successfully. performance_glitch_user
        # has a deliberate multi-second delay before the redirect fires,
        # so this must wait for it rather than checking current_url right
        # after the click.
        for user in [config.PROBLEM_USER, config.PERFORMANCE_GLITCH_USER,
                     config.ERROR_USER, config.VISUAL_USER]:
            with self.subTest(user=user):
                self.login_page.load()
                self.login_page.login(user, config.PASSWORD)
                self.login_page.wait_for_url_contains("inventory.html")
                self.assertIn("inventory.html", self.driver.current_url)

    def test_ULF_007_login_button_fail(self):
        self.login_page.login(config.STANDARD_USER, "wrong_password")
        self.assertTrue(self.login_page.is_error_displayed())
        self.assertIn("do not match", self.login_page.get_error_text().lower())
        self.assertNotIn("inventory.html", self.driver.current_url)

    def test_ULF_008_login_no_username(self):
        self.login_page.login("", config.PASSWORD)
        self.assertTrue(self.login_page.is_error_displayed())
        self.assertIn("username is required", self.login_page.get_error_text().lower())

    def test_ULF_009_login_no_password(self):
        self.login_page.login(config.STANDARD_USER, "")
        self.assertTrue(self.login_page.is_error_displayed())
        self.assertIn("password is required", self.login_page.get_error_text().lower())

    def test_ULF_010_login_attempts_repeated_failures_stay_usable(self):
        # saucedemo doesn't lock accounts based on attempt count, so this
        # verifies the form stays responsive and correct across repeats.
        for _ in range(3):
            self.login_page.login(config.STANDARD_USER, "wrong_password")
            self.assertTrue(self.login_page.is_error_displayed())
            self.login_page.close_error()
        self.login_page.login(config.STANDARD_USER, config.PASSWORD)
        self.assertIn("inventory.html", self.driver.current_url)

    def test_ULF_011_user_lockout(self):
        self.login_page.login(config.LOCKED_OUT_USER, config.PASSWORD)
        self.assertTrue(self.login_page.is_error_displayed())
        self.assertIn("locked out", self.login_page.get_error_text().lower())

    def test_error_message_can_be_closed(self):
        self.login_page.login("", "")
        self.assertTrue(self.login_page.is_error_displayed())
        self.login_page.close_error()
        self.assertFalse(self.login_page.is_error_displayed())

    # --- GLB-001..003 ---
    def test_GLB_001_invalid_username_invalid_password(self):
        self.login_page.login("no_such_user", "wrong_password")
        self.assertTrue(self.login_page.is_error_displayed())
        self.assertIn("do not match", self.login_page.get_error_text().lower())

    def test_GLB_002_no_username_no_password(self):
        self.login_page.login("", "")
        self.assertTrue(self.login_page.is_error_displayed())
        self.assertIn("username is required", self.login_page.get_error_text().lower())

    def test_GLB_003_login_button_locked_user(self):
        self.login_page.login(config.LOCKED_OUT_USER, config.PASSWORD)
        self.assertTrue(self.login_page.is_error_displayed())
        self.assertIn("locked out", self.login_page.get_error_text().lower())


class LogoutTests(unittest.TestCase):
    """ULF-012..020"""

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        login_page = LoginPage(self.driver)
        login_page.load()
        login_page.login(config.STANDARD_USER, config.PASSWORD)
        self.inventory_page = InventoryPage(self.driver)
        self.login_page = LoginPage(self.driver)

    def tearDown(self):
        self.driver.quit()

    def test_ULF_012_user_logout(self):
        self.inventory_page.logout()
        self.assertEqual(self.driver.current_url, config.BASE_URL)

    def test_ULF_013_user_logout_button(self):
        self.inventory_page.open_sidebar()
        from selenium.webdriver.common.by import By
        logout_link = self.driver.find_element(By.ID, "logout_sidebar_link")
        self.assertTrue(logout_link.is_displayed())

    @unittest.skip("saucedemo.com has no logout confirmation dialog - clicking Logout logs out immediately")
    def test_ULF_014_user_logout_confirmation(self):
        pass

    @unittest.skip("saucedemo.com has no logout confirmation dialog - no Confirm button exists")
    def test_ULF_015_user_logout_confirmation_confirm_button(self):
        pass

    @unittest.skip("saucedemo.com has no logout confirmation dialog - no Cancel button exists")
    def test_ULF_016_user_logout_confirmation_cancel_button(self):
        pass

    def test_ULF_017_logged_out_page(self):
        self.inventory_page.logout()
        self.assertTrue(self.login_page.is_username_enabled())
        self.assertTrue(self.login_page.is_password_enabled())
        self.assertTrue(self.login_page.is_login_button_enabled())

    @unittest.skip("saucedemo.com has no session-timeout/inactivity feature to exercise")
    def test_ULF_018_logged_out_page_inactivity(self):
        pass

    def test_ULF_019_logged_out_page_session(self):
        self.inventory_page.logout()
        # Directly requesting an authenticated page after logout must not
        # grant access - saucedemo bounces this back to "/" with an error.
        self.driver.get("https://www.saucedemo.com/inventory.html")
        self.assertNotIn("inventory.html", self.driver.current_url)

    def test_ULF_020_logged_out_page_back(self):
        self.inventory_page.logout()
        self.driver.back()
        self.assertNotIn("inventory.html", self.driver.current_url)


if __name__ == "__main__":
    unittest.main()
