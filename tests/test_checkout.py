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
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        login_page = LoginPage(self.driver)
        login_page.load()
        login_page.login(config.STANDARD_USER, config.PASSWORD)
        inventory_page = InventoryPage(self.driver)
        inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")
        inventory_page.go_to_cart()
        CartPage(self.driver).checkout()
        self.step_one = CheckoutStepOnePage(self.driver)

    def tearDown(self):
        self.driver.quit()

    def test_valid_info_proceeds_to_step_two(self):
        self.step_one.fill_info("John", "Doe", "12345")
        self.step_one.continue_checkout()
        self.assertIn("checkout-step-two.html", self.driver.current_url)

    def test_missing_first_name_shows_error(self):
        self.step_one.fill_info("", "Doe", "12345")
        self.step_one.continue_checkout()
        self.assertTrue(self.step_one.is_error_displayed())
        self.assertIn("first name is required", self.step_one.get_error_text().lower())

    def test_missing_last_name_shows_error(self):
        self.step_one.fill_info("John", "", "12345")
        self.step_one.continue_checkout()
        self.assertTrue(self.step_one.is_error_displayed())
        self.assertIn("last name is required", self.step_one.get_error_text().lower())

    def test_missing_postal_code_shows_error(self):
        self.step_one.fill_info("John", "Doe", "")
        self.step_one.continue_checkout()
        self.assertTrue(self.step_one.is_error_displayed())
        self.assertIn("postal code is required", self.step_one.get_error_text().lower())

    def test_cancel_returns_to_cart(self):
        self.step_one.cancel()
        self.assertIn("cart.html", self.driver.current_url)


class CheckoutStepTwoTests(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        login_page = LoginPage(self.driver)
        login_page.load()
        login_page.login(config.STANDARD_USER, config.PASSWORD)
        inventory_page = InventoryPage(self.driver)
        inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")
        inventory_page.add_item_to_cart_by_name("Sauce Labs Bike Light")
        inventory_page.go_to_cart()
        CartPage(self.driver).checkout()
        step_one = CheckoutStepOnePage(self.driver)
        step_one.fill_info("John", "Doe", "12345")
        step_one.continue_checkout()
        self.step_two = CheckoutStepTwoPage(self.driver)

    def tearDown(self):
        self.driver.quit()

    def test_step_two_shows_correct_item_count(self):
        self.assertEqual(self.step_two.get_cart_item_count(), 2)

    def test_total_equals_subtotal_plus_tax(self):
        subtotal = self.step_two.get_subtotal()
        tax = self.step_two.get_tax()
        total = self.step_two.get_total()
        self.assertAlmostEqual(subtotal + tax, total, places=2)

    def test_cancel_returns_to_inventory(self):
        self.step_two.cancel()
        self.assertIn("inventory.html", self.driver.current_url)

    def test_finish_completes_order(self):
        self.step_two.finish()
        self.assertIn("checkout-complete.html", self.driver.current_url)


class CheckoutCompleteTests(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        login_page = LoginPage(self.driver)
        login_page.load()
        login_page.login(config.STANDARD_USER, config.PASSWORD)
        inventory_page = InventoryPage(self.driver)
        inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")
        inventory_page.go_to_cart()
        CartPage(self.driver).checkout()
        step_one = CheckoutStepOnePage(self.driver)
        step_one.fill_info("John", "Doe", "12345")
        step_one.continue_checkout()
        step_two = CheckoutStepTwoPage(self.driver)
        step_two.finish()
        self.complete_page = CheckoutCompletePage(self.driver)

    def tearDown(self):
        self.driver.quit()

    def test_completion_message_displayed(self):
        self.assertTrue(self.complete_page.is_loaded())
        self.assertIn("thank you", self.complete_page.get_header_text().lower())

    def test_back_home_returns_to_inventory(self):
        self.complete_page.back_home()
        self.assertIn("inventory.html", self.driver.current_url)


if __name__ == "__main__":
    unittest.main()