from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CartPage(BasePage):
    URL = "https://www.saucedemo.com/cart.html"
    CART_TITLE = (By.CLASS_NAME, "title")  # "Your Cart"
    CART_ITEM = (By.CLASS_NAME, "cart_item")
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    ITEM_QUANTITY = (By.CLASS_NAME, "cart_quantity")
    CONTINUE_SHOPPING_BUTTON = (By.ID, "continue-shopping")
    CHECKOUT_BUTTON = (By.ID, "checkout")

    # --- CCF-002/007: Cart page redirect / "Your Cart" heading ---
    def is_loaded(self):
        return "cart.html" in self.current_url()

    def get_page_title(self):
        return self.get_text(self.CART_TITLE)

    # --- CCF-010: item count / quantities in cart ---
    def get_cart_item_count(self):
        try:
            return len(self.find_all(self.CART_ITEM))
        except Exception:
            return 0

    def get_item_names(self):
        try:
            return [el.text for el in self.find_all(self.ITEM_NAME)]
        except Exception:
            return []

    def get_item_quantities(self):
        try:
            return [int(el.text) for el in self.find_all(self.ITEM_QUANTITY)]
        except Exception:
            return []

    def remove_item_by_name(self, name):
        formatted_name = name.lower().replace(" ", "-")
        self.click((By.ID, f"remove-{formatted_name}"))

    # --- CCF-008: Continue Shopping button ---
    def continue_shopping(self):
        self.click(self.CONTINUE_SHOPPING_BUTTON)
        self.wait_for_url_contains("inventory.html")

    # --- CCF-009: Checkout button ---
    def checkout(self):
        self.click(self.CHECKOUT_BUTTON)
        self.wait_for_url_contains("checkout-step-one.html")
