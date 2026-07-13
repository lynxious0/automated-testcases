import unittest
from selenium import webdriver
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.product_page import ProductPage
from tests import config


class ProductDetailTests(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        login_page = LoginPage(self.driver)
        login_page.load()
        login_page.login(config.STANDARD_USER, config.PASSWORD)
        self.inventory_page = InventoryPage(self.driver)
        self.inventory_page.click_item_name("Sauce Labs Backpack")
        self.product_page = ProductPage(self.driver)

    def tearDown(self):
        self.driver.quit()

    def test_product_detail_loads_correct_item(self):
        self.assertTrue(self.product_page.is_loaded())
        self.assertEqual(self.product_page.get_item_name(), "Sauce Labs Backpack")

    def test_add_to_cart_from_detail_page(self):
        self.product_page.add_to_cart()
        self.assertTrue(self.inventory_page.is_visible(self.inventory_page.CART_BADGE))
        self.assertEqual(self.inventory_page.get_cart_badge_count(), 1)

    def test_remove_from_cart_on_detail_page(self):
        self.product_page.add_to_cart()
        self.product_page.remove_from_cart()
        self.assertEqual(self.inventory_page.get_cart_badge_count(), 0)

    def test_back_button_returns_to_inventory(self):
        self.product_page.go_back()
        self.assertTrue(self.inventory_page.is_loaded())


if __name__ == "__main__":
    unittest.main()