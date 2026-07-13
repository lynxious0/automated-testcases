"""Covers the Cart & Checkout Feature: Cart section (CCF-001..010)."""
import unittest
from selenium import webdriver
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.product_page import ProductPage
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

    def test_CCF_001_cart_icon(self):
        self.inventory_page.go_to_cart()
        self.assertIn("cart.html", self.driver.current_url)

    def test_CCF_002_cart_page_redirect(self):
        self.inventory_page.go_to_cart()
        self.assertTrue(self.cart_page.is_loaded())

    def test_CCF_003_page_list_add_to_cart(self):
        self.inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")
        self.assertEqual(self.inventory_page.get_cart_badge_count(), 1)

    def test_CCF_004_page_list_remove_button(self):
        self.inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")
        self.inventory_page.remove_item_from_cart_by_name("Sauce Labs Backpack")
        self.assertEqual(self.inventory_page.get_cart_badge_count(), 0)

    def test_CCF_005_product_page_add_to_cart_button(self):
        self.inventory_page.click_item_name("Sauce Labs Backpack")
        product_page = ProductPage(self.driver)
        product_page.add_to_cart()
        self.assertEqual(self.inventory_page.get_cart_badge_count(), 1)

    def test_CCF_006_product_page_remove_button(self):
        self.inventory_page.click_item_name("Sauce Labs Backpack")
        product_page = ProductPage(self.driver)
        product_page.add_to_cart()
        product_page.remove_from_cart()
        self.assertEqual(self.inventory_page.get_cart_badge_count(), 0)

    def test_CCF_007_cart_page_your_cart(self):
        self.inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")
        self.inventory_page.add_item_to_cart_by_name("Sauce Labs Bike Light")
        self.inventory_page.go_to_cart()
        self.assertIn("your cart", self.cart_page.get_page_title().lower())
        self.assertEqual(self.cart_page.get_cart_item_count(), 2)
        names = self.cart_page.get_item_names()
        self.assertIn("Sauce Labs Backpack", names)
        self.assertIn("Sauce Labs Bike Light", names)

    def test_CCF_008_cart_page_continue_shopping_button(self):
        self.inventory_page.go_to_cart()
        self.cart_page.continue_shopping()
        self.assertTrue(self.inventory_page.is_loaded())

    def test_CCF_009_cart_page_checkout_button(self):
        self.inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")
        self.inventory_page.go_to_cart()
        self.cart_page.checkout()
        self.assertIn("checkout-step-one.html", self.driver.current_url)

    def test_CCF_010_cart_page_checkout_item_items(self):
        self.inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")
        self.inventory_page.add_item_to_cart_by_name("Sauce Labs Bike Light")
        self.inventory_page.go_to_cart()
        self.assertEqual(self.cart_page.get_cart_item_count(), 2)
        quantities = self.cart_page.get_item_quantities()
        self.assertEqual(quantities, [1, 1])


if __name__ == "__main__":
    unittest.main()
