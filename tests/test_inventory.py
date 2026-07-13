import unittest
from selenium import webdriver
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.product_page import ProductPage
from tests import config


class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        login_page = LoginPage(self.driver)
        login_page.load()
        login_page.login(config.STANDARD_USER, config.PASSWORD)
        self.inventory_page = InventoryPage(self.driver)

    def tearDown(self):
        self.driver.quit()

    def test_inventory_page_loads_with_six_items(self):
        self.assertTrue(self.inventory_page.is_loaded())
        self.assertEqual(self.inventory_page.get_item_count(), 6)

    def test_sort_name_a_to_z(self):
        self.inventory_page.sort_by("az")
        names = self.inventory_page.get_item_names()
        self.assertEqual(names, sorted(names))

    def test_sort_name_z_to_a(self):
        self.inventory_page.sort_by("za")
        names = self.inventory_page.get_item_names()
        self.assertEqual(names, sorted(names, reverse=True))

    def test_sort_price_low_to_high(self):
        self.inventory_page.sort_by("lohi")
        prices = self.inventory_page.get_item_prices()
        self.assertEqual(prices, sorted(prices))

    def test_sort_price_high_to_low(self):
        self.inventory_page.sort_by("hilo")
        prices = self.inventory_page.get_item_prices()
        self.assertEqual(prices, sorted(prices, reverse=True))

    def test_add_single_item_to_cart_updates_badge(self):
        self.inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")
        self.assertEqual(self.inventory_page.get_cart_badge_count(), 1)

    def test_add_multiple_items_to_cart_updates_badge(self):
        self.inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")
        self.inventory_page.add_item_to_cart_by_name("Sauce Labs Bike Light")
        self.assertEqual(self.inventory_page.get_cart_badge_count(), 2)

    def test_remove_item_from_cart_updates_badge(self):
        self.inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")
        self.inventory_page.remove_item_from_cart_by_name("Sauce Labs Backpack")
        self.assertEqual(self.inventory_page.get_cart_badge_count(), 0)

    def test_click_item_name_opens_product_detail(self):
        self.inventory_page.click_item_name("Sauce Labs Backpack")
        product_page = ProductPage(self.driver)
        self.assertTrue(product_page.is_loaded())
        self.assertEqual(product_page.get_item_name(), "Sauce Labs Backpack")

    def test_go_to_cart_navigates_to_cart_page(self):
        self.inventory_page.go_to_cart()
        self.assertIn("cart.html", self.driver.current_url)

    def test_reset_app_state_clears_cart(self):
        self.inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")
        self.assertEqual(self.inventory_page.get_cart_badge_count(), 1)
        self.inventory_page.reset_app_state()
        self.assertEqual(self.inventory_page.get_cart_badge_count(), 0)

    def test_about_link_redirects_to_saucelabs(self):
        self.inventory_page.click_about()
        self.driver.implicitly_wait(3)
        self.assertIn("saucelabs.com", self.driver.current_url)

    def test_logout_returns_to_login_page(self):
        self.inventory_page.logout()
        self.assertEqual(self.driver.current_url, "https://www.saucedemo.com/")


if __name__ == "__main__":
    unittest.main()