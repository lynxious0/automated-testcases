import unittest
from selenium import webdriver
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from tests import config


class CartTests(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        login_page = LoginPage(self.driver)
        login_page.load()
        login_page.login(config.STANDARD_USER, config.PASSWORD)
        self.inventory_page = InventoryPage(self.driver)
        self.cart_page = CartPage(self.driver)

    def tearDown(self):
        self.driver.quit()

    def test_cart_shows_added_items(self):
        self.inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")
        self.inventory_page.add_item_to_cart_by_name("Sauce Labs Bike Light")
        self.inventory_page.go_to_cart()
        self.assertEqual(self.cart_page.get_cart_item_count(), 2)
        names = self.cart_page.get_item_names()
        self.assertIn("Sauce Labs Backpack", names)
        self.assertIn("Sauce Labs Bike Light", names)

    def test_empty_cart_shows_zero_items(self):
        self.inventory_page.go_to_cart()
        self.assertEqual(self.cart_page.get_cart_item_count(), 0)

    def test_remove_item_from_cart_page(self):
        self.inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")
        self.inventory_page.go_to_cart()
        self.cart_page.remove_item_by_name("Sauce Labs Backpack")
        self.assertEqual(self.cart_page.get_cart_item_count(), 0)

    def test_continue_shopping_returns_to_inventory(self):
        self.inventory_page.go_to_cart()
        self.cart_page.continue_shopping()
        self.assertTrue(self.inventory_page.is_loaded())

    def test_checkout_button_navigates_to_checkout(self):
        self.inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")
        self.inventory_page.go_to_cart()
        self.cart_page.checkout()
        self.assertIn("checkout-step-one.html", self.driver.current_url)


if __name__ == "__main__":
    unittest.main()