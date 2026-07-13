from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class ProductPage(BasePage):
    ITEM_NAME = (By.CLASS_NAME, "inventory_details_name")
    ITEM_DESC = (By.CLASS_NAME, "inventory_details_desc")
    ITEM_PRICE = (By.CLASS_NAME, "inventory_details_price")
    ITEM_IMAGE = (By.CSS_SELECTOR, ".inventory_details_img")
    ADD_TO_CART_BUTTON = (By.XPATH, "//button[contains(@id, 'add-to-cart')]")
    REMOVE_BUTTON = (By.XPATH, "//button[contains(@id, 'remove')]")
    BACK_BUTTON = (By.ID, "back-to-products")

    # --- PPF-007..013: Product Page ---
    def is_loaded(self):
        return self.is_visible(self.ITEM_NAME)

    def get_item_name(self):
        return self.get_text(self.ITEM_NAME)

    def get_item_description(self):
        return self.get_text(self.ITEM_DESC)

    def get_item_price(self):
        return float(self.get_text(self.ITEM_PRICE).replace("$", ""))

    def add_to_cart(self):
        self.click(self.ADD_TO_CART_BUTTON)
        return self

    def remove_from_cart(self):
        self.click(self.REMOVE_BUTTON)
        return self

    def go_back(self):
        self.click(self.BACK_BUTTON)
        self.wait_for_url_contains("inventory.html")
        return self
