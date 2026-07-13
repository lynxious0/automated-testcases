from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage


class InventoryPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.INVENTORY_CONTAINER = (By.ID, "inventory_container")
        self.ITEM_CARDS = (By.CLASS_NAME, "inventory_item")
        self.ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
        self.ITEM_DESCS = (By.CLASS_NAME, "inventory_item_desc")
        self.ITEM_IMAGES = (By.CSS_SELECTOR, ".inventory_item_img img")
        self.ITEM_PRICES = (By.CLASS_NAME, "inventory_item_price")
        self.SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
        self.CART_BUTTON = (By.CLASS_NAME, "shopping_cart_link")
        self.CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")

    # --- PPF-001..006: Product List ---
    def is_loaded(self):
        return self.is_visible(self.INVENTORY_CONTAINER)

    def get_item_count(self):
        return len(self.find_all(self.ITEM_CARDS))

    def get_item_names(self):
        return [el.text for el in self.find_all(self.ITEM_NAMES)]

    def get_item_descriptions(self):
        return [el.text for el in self.find_all(self.ITEM_DESCS)]

    def get_item_image_srcs(self):
        return [el.get_attribute("src") for el in self.find_all(self.ITEM_IMAGES)]

    def get_item_prices(self):
        return [float(el.text.replace("$", "")) for el in self.find_all(self.ITEM_PRICES)]

    # --- PPF-014..017: Product Filter (sort dropdown) ---
    def sort_by(self, value):
        Select(self.find(self.SORT_DROPDOWN)).select_by_value(value)

    def get_selected_sort_label(self):
        return Select(self.find(self.SORT_DROPDOWN)).first_selected_option.text

    # --- Cart interactions (CCF-003/004) ---
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
        for el in self.find_all(self.ITEM_NAMES):
            if el.text == name:
                el.click()
                return
        raise ValueError(f"Item '{name}' not found on inventory page")

    def go_to_cart(self):
        self.click(self.CART_BUTTON)
        self.wait_for_url_contains("cart.html")

    # --- Sidebar menu ---
    def open_sidebar(self):
        self.click((By.ID, "react-burger-menu-btn"))
        self.wait.until(lambda d: self.is_visible((By.ID, "logout_sidebar_link")))

    def js_click(self, locator):
        element = self.find(locator)
        self.driver.execute_script("arguments[0].click();", element)

    def click_about(self):
        self.open_sidebar()
        self.js_click((By.ID, "about_sidebar_link"))

    def logout(self):
        self.open_sidebar()
        self.js_click((By.ID, "logout_sidebar_link"))
        self.wait_for_url_contains("saucedemo.com")

    def reset_app_state(self):
        self.open_sidebar()
        self.js_click((By.ID, "reset_sidebar_link"))
