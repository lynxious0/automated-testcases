"""
Covers the Cart & Checkout Feature: Checkout section (CCF-011..025).

CCF-015 Checkout Page Payment Input Field is marked skip() - the
saucedemo.com checkout form only collects first name, last name, and
postal code. There is no payment/card input field on this site.
"""
import unittest
from selenium import webdriver
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_step_one_page import CheckoutStepOnePage
from pages.checkout_step_two_page import CheckoutStepTwoPage
from pages.checkout_complete_page import CheckoutCompletePage
from tests import config


class CheckoutStepOneTests(unittest.TestCase):
    """CCF-011..019"""

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        login_page = LoginPage(self.driver)
        login_page.load()
        login_page.login(config.STANDARD_USER, config.PASSWORD)
        login_page.wait_for_url_contains("inventory.html")
        inventory_page = InventoryPage(self.driver)
        inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")
        inventory_page.go_to_cart()
        CartPage(self.driver).checkout()
        self.step_one = CheckoutStepOnePage(self.driver)

    def tearDown(self):
        self.driver.quit()

    def test_CCF_011_checkout_page(self):
        self.assertTrue(self.step_one.is_loaded())

    def test_CCF_012_checkout_page_first_name_input_field(self):
        self.step_one.enter_first_name("John")
        value = self.driver.find_element(*self.step_one.FIRST_NAME_FIELD).get_attribute("value")
        self.assertEqual(value, "John")

    def test_CCF_013_checkout_page_last_name_input_field(self):
        self.step_one.enter_last_name("Doe")
        value = self.driver.find_element(*self.step_one.LAST_NAME_FIELD).get_attribute("value")
        self.assertEqual(value, "Doe")

    def test_CCF_014_checkout_page_postal_code_input_field(self):
        self.step_one.enter_postal_code("12345")
        value = self.driver.find_element(*self.step_one.POSTAL_CODE_FIELD).get_attribute("value")
        self.assertEqual(value, "12345")

    @unittest.skip("saucedemo.com's checkout form has no payment input field to test")
    def test_CCF_015_checkout_page_payment_input_field(self):
        pass

    def test_CCF_016_checkout_page_back_button(self):
        self.step_one.cancel()
        self.assertIn("cart.html", self.driver.current_url)

    def test_CCF_017_checkout_page_continue_button(self):
        continue_btn = self.driver.find_element(*self.step_one.CONTINUE_BUTTON)
        self.assertTrue(continue_btn.is_enabled())

    def test_CCF_018_checkout_page_continue_button_fail(self):
        self.step_one.fill_info("", "Doe", "12345")
        self.step_one.continue_checkout()
        self.assertTrue(self.step_one.is_error_displayed())
        self.assertIn("first name is required", self.step_one.get_error_text().lower())

        self.step_one.enter_first_name("John")
        self.driver.find_element(*self.step_one.LAST_NAME_FIELD).clear()
        self.step_one.continue_checkout()
        self.assertTrue(self.step_one.is_error_displayed())
        self.assertIn("last name is required", self.step_one.get_error_text().lower())

        self.step_one.enter_last_name("Doe")
        self.driver.find_element(*self.step_one.POSTAL_CODE_FIELD).clear()
        self.step_one.continue_checkout()
        self.assertTrue(self.step_one.is_error_displayed())
        self.assertIn("postal code is required", self.step_one.get_error_text().lower())

    def test_CCF_019_checkout_page_continue_button_success(self):
        self.step_one.fill_info("John", "Doe", "12345")
        self.step_one.continue_checkout()
        self.step_one.wait_for_url_contains("checkout-step-two.html")
        self.assertIn("checkout-step-two.html", self.driver.current_url)


class CheckoutConfirmationTests(unittest.TestCase):
    """CCF-020..022"""

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        login_page = LoginPage(self.driver)
        login_page.load()
        login_page.login(config.STANDARD_USER, config.PASSWORD)
        login_page.wait_for_url_contains("inventory.html")
        inventory_page = InventoryPage(self.driver)
        inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")
        inventory_page.add_item_to_cart_by_name("Sauce Labs Bike Light")
        inventory_page.go_to_cart()
        CartPage(self.driver).checkout()
        step_one = CheckoutStepOnePage(self.driver)
        step_one.fill_info("John", "Doe", "12345")
        step_one.continue_checkout()
        step_one.wait_for_url_contains("checkout-step-two.html")
        self.step_two = CheckoutStepTwoPage(self.driver)

    def tearDown(self):
        self.driver.quit()

    def test_CCF_020_checkout_confirmation(self):
        self.assertTrue(self.step_two.is_loaded())
        self.assertEqual(self.step_two.get_cart_item_count(), 2)
        subtotal = self.step_two.get_subtotal()
        tax = self.step_two.get_tax()
        total = self.step_two.get_total()
        self.assertAlmostEqual(subtotal + tax, total, places=2)

    def test_CCF_021_checkout_confirmation_back_button(self):
        self.step_two.cancel()
        self.assertIn("inventory.html", self.driver.current_url)

    def test_CCF_022_checkout_confirmation_finish(self):
        self.step_two.finish()
        self.assertIn("checkout-complete.html", self.driver.current_url)


class CheckoutCompleteTests(unittest.TestCase):
    """CCF-023..025"""

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        login_page = LoginPage(self.driver)
        login_page.load()
        login_page.login(config.STANDARD_USER, config.PASSWORD)
        login_page.wait_for_url_contains("inventory.html")
        inventory_page = InventoryPage(self.driver)
        inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")
        inventory_page.go_to_cart()
        CartPage(self.driver).checkout()
        step_one = CheckoutStepOnePage(self.driver)
        step_one.fill_info("John", "Doe", "12345")
        step_one.continue_checkout()
        step_one.wait_for_url_contains("checkout-step-two.html")
        step_two = CheckoutStepTwoPage(self.driver)
        step_two.finish()
        self.complete_page = CheckoutCompletePage(self.driver)

    def tearDown(self):
        self.driver.quit()

    def test_CCF_023_checkout_complete(self):
        self.assertTrue(self.complete_page.is_loaded())
        self.assertIn("thank you", self.complete_page.get_header_text().lower())

    def test_CCF_024_checkout_complete_button(self):
        back_btn = self.driver.find_element(*self.complete_page.BACK_HOME_BUTTON)
        self.assertTrue(back_btn.is_displayed())
        self.assertTrue(back_btn.is_enabled())

    def test_CCF_025_checkout_complete_click_go_back(self):
        self.complete_page.back_home()
        self.assertIn("inventory.html", self.driver.current_url)


if __name__ == "__main__":
    unittest.main()
