"""
Covers the Product Feature: Product Page section (PPF-007..013).

Two IDs are marked skip() - saucedemo.com's product detail page has
no matching UI:
  PPF-010 Product Description Price Localization -> single currency (USD) only
  PPF-011 Product Page Rating -> no star-rating element
  PPF-012 Product Page Quantity -> no quantity stepper/selector on this page
"""
import unittest
from selenium import webdriver
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.product_page import ProductPage
from tests import config


class ProductPageTests(unittest.TestCase):
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

    def test_PPF_007_product_page_redirect(self):
        self.assertTrue(self.product_page.is_loaded())
        self.assertIn("inventory-item.html", self.driver.current_url)
        self.assertEqual(self.product_page.get_item_name(), "Sauce Labs Backpack")

    def test_PPF_008_product_page_description(self):
        self.assertTrue(self.product_page.get_item_description().strip())

    def test_PPF_009_product_description_price(self):
        self.assertGreater(self.product_page.get_item_price(), 0)

    @unittest.skip("saucedemo.com only displays a single currency (USD) - no localization to test")
    def test_PPF_010_product_description_price_localization(self):
        pass

    @unittest.skip("saucedemo.com's product page has no star-rating element to test")
    def test_PPF_011_product_page_rating(self):
        pass

    @unittest.skip("saucedemo.com's product page has no quantity selector/stepper to test")
    def test_PPF_012_product_page_quantity(self):
        pass

    def test_PPF_013_product_description_back_to_products_button(self):
        self.product_page.go_back()
        self.assertTrue(self.inventory_page.is_loaded())


if __name__ == "__main__":
    unittest.main()
