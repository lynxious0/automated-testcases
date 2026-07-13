from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage


class InventoryPage(BasePage):
    HEADER_LABEL = (By.CLASS_NAME, "app_logo")
    INVENTORY_ITEM = (By.CLASS_NAME, "inventory_item")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICE = (By.CLASS_NAME, "inventory_item_price")
    BURGER_MENU = (By.ID, "react-burger-menu-btn")
    ABOUT_LINK = (By.ID, "about_sidebar_link")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")
    RESET_LINK = (By.ID, "reset_sidebar_link")

    def is_loaded(self):
        return self.is_visible(self.HEADER_LABEL)

    def get_item_count(self):
        try:
            return len(self.find_all(self.INVENTORY_ITEM))
        except:
            return 0

    def get_item_names(self):
        return [el.text for el in self.find_all(self.ITEM_NAME)]

    def get_item_prices(self):
        return [float(el.text.replace("$", "")) for el in self.find_all(self.ITEM_PRICE)]

    def click_item_name(self, name):
        items = self.find_all(self.ITEM_NAME)
        for item in items:
            if item.text == name:
                item.click()
                break

    def sort_by(self, option_value):
        select = Select(self.find(self.SORT_DROPDOWN))
        select.select_by_value(option_value)

    def get_cart_badge_count(self):
        if self.is_visible(self.CART_BADGE):
            return int(self.get_text(self.CART_BADGE))
        return 0

    def add_item_to_cart_by_name(self, name):
        formatted_name = name.lower().replace(" ", "-")
        locator = (By.ID, f"add-to-cart-{formatted_name}")
        self.click(locator)

    def remove_item_from_cart_by_name(self, name):
        formatted_name = name.lower().replace(" ", "-")
        locator = (By.ID, f"remove-{formatted_name}")
        self.click(locator)

    def go_to_cart(self):
        self.click(self.CART_LINK)

    def click_about(self):
        self.click(self.BURGER_MENU)
        self.click(self.ABOUT_LINK)

    def logout(self):
        self.click(self.BURGER_MENU)
        self.click(self.LOGOUT_LINK)

    def reset_app_state(self):
        self.click(self.BURGER_MENU)
        self.click(self.RESET_LINK)