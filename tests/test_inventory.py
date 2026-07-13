"""
Covers the Product Feature: Product List (PPF-001..006) and Product
Filter (PPF-014..017) sections of the test case docs.

PPF-005 Product List Rating is marked skip() - saucedemo.com's product
list has no star-rating UI to test.
"""
import unittest
from selenium import webdriver
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from tests import config


class ProductListTests(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        login_page = LoginPage(self.driver)
        login_page.load()
        login_page.login(config.STANDARD_USER, config.PASSWORD)
        self.inventory_page = InventoryPage(self.driver)

    def tearDown(self):
        self.driver.quit()

    def test_PPF_001_product_list_name(self):
        names = self.inventory_page.get_item_names()
        self.assertEqual(len(names), 6)
        self.assertTrue(all(name.strip() for name in names))

    def test_PPF_002_product_list_image(self):
        srcs = self.inventory_page.get_item_image_srcs()
        self.assertEqual(len(srcs), 6)
        self.assertTrue(all(src for src in srcs))

    def test_PPF_003_product_list_description(self):
        descriptions = self.inventory_page.get_item_descriptions()
        self.assertEqual(len(descriptions), 6)
        self.assertTrue(all(desc.strip() for desc in descriptions))

    def test_PPF_004_product_list_price(self):
        prices = self.inventory_page.get_item_prices()
        self.assertEqual(len(prices), 6)
        self.assertTrue(all(price > 0 for price in prices))

    @unittest.skip("saucedemo.com's product list has no star-rating element to test")
    def test_PPF_005_product_list_rating(self):
        pass

    def test_PPF_006_product_list_quantity(self):
        self.assertTrue(self.inventory_page.is_loaded())
        self.assertEqual(self.inventory_page.get_item_count(), 6)


class ProductFilterTests(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        login_page = LoginPage(self.driver)
        login_page.load()
        login_page.login(config.STANDARD_USER, config.PASSWORD)
        self.inventory_page = InventoryPage(self.driver)

    def tearDown(self):
        self.driver.quit()

    def test_PPF_014_product_filter_a_to_z(self):
        self.inventory_page.sort_by("az")
        names = self.inventory_page.get_item_names()
        self.assertEqual(names, sorted(names))

    def test_PPF_015_product_filter_z_to_a(self):
        self.inventory_page.sort_by("za")
        names = self.inventory_page.get_item_names()
        self.assertEqual(names, sorted(names, reverse=True))

    def test_PPF_016_product_filter_price_high_to_low(self):
        self.inventory_page.sort_by("hilo")
        prices = self.inventory_page.get_item_prices()
        self.assertEqual(prices, sorted(prices, reverse=True))

    def test_PPF_017_product_filter_price_low_to_high(self):
        self.inventory_page.sort_by("lohi")
        prices = self.inventory_page.get_item_prices()
        self.assertEqual(prices, sorted(prices))


if __name__ == "__main__":
    unittest.main()
