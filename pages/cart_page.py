from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CartPage(BasePage):
    CART_ITEM = (By.CLASS_NAME, "cart_item")
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    CONTINUE_SHOPPING_BUTTON = (By.ID, "continue-shopping")
    CHECKOUT_BUTTON = (By.ID, "checkout")

    def get_cart_item_count(self):
        try:
            return len(self.find_all(self.CART_ITEM))
        except:
            return 0

    def get_item_names(self):
        try:
            return [el.text for el in self.find_all(self.ITEM_NAME)]
        except:
            return []

    def remove_item_by_name(self, name):
        formatted_name = name.lower().replace(" ", "-")
        locator = (By.ID, f"remove-{formatted_name}")
        self.click(locator)

    def continue_shopping(self):
        self.click(self.CONTINUE_SHOPPING_BUTTON)

    def checkout(self):
        self.click(self.CHECKOUT_BUTTON)