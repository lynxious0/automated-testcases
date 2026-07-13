import time
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class InventoryPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.INVENTORY_CONTAINER = (By.ID, "inventory_container")
        self.ITEM_CARDS = (By.CLASS_NAME, "inventory_item")
        self.ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
        self.ITEM_PRICES = (By.CLASS_NAME, "inventory_item_price")
        self.SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
        self.CART_BUTTON = (By.CLASS_NAME, "shopping_cart_link")
        self.CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")

    def is_loaded(self):
        return self.is_visible(self.INVENTORY_CONTAINER)

    def get_item_count(self):
        return len(self.find_all(self.ITEM_CARDS))

    def get_item_names(self):
        elements = self.find_all(self.ITEM_NAMES)
        return [el.text for el in elements]

    def get_item_prices(self):
        elements = self.find_all(self.ITEM_PRICES)
        return [float(el.text.replace("$", "")) for el in elements]

    def sort_by(self, value):
        from selenium.webdriver.support.ui import Select
        dropdown = Select(self.find(self.SORT_DROPDOWN))
        dropdown.select_by_value(value)

    def add_item_to_cart_by_name(self, name):
        button_id = f"add-to-cart-{name.lower().replace(' ', '-')}"
        self.click((By.ID, button_id))

    def remove_item_from_cart_by_name(self, name):
        button_id = f"remove-{name.lower().replace(' ', '-')}"
        self.click((By.ID, button_id))

    def get_cart_badge_count(self):
        try:
            return int(self.find(self.CART_BADGE).text)
        except Exception:
            return 0

    def click_item_name(self, name):
        elements = self.find_all(self.ITEM_NAMES)
        for el in elements:
            if el.text == name:
                el.click()
                break

    def go_to_cart(self):
        self.click(self.CART_BUTTON)

    def open_sidebar(self):
        self.click((By.ID, "react-burger-menu-btn"))
        time.sleep(1)

    def js_click(self, locator):
        element = self.find(locator)
        self.driver.execute_script("arguments[0].click();", element)

    def click_about(self):
        self.open_sidebar()
        self.js_click((By.ID, "about_sidebar_link"))
        time.sleep(2)

    def logout(self):
        self.open_sidebar()
        self.js_click((By.ID, "logout_sidebar_link"))
        time.sleep(1.5)

    def reset_app_state(self):
        self.open_sidebar()
        self.js_click((By.ID, "reset_sidebar_link"))
        time.sleep(1)