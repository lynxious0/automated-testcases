import time
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CheckoutStepTwoPage(BasePage):
    URL = "https://www.saucedemo.com/checkout-step-two.html"

    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    ITEM_TOTAL = (By.CLASS_NAME, "summary_subtotal_label")
    TAX_LABEL = (By.CLASS_NAME, "summary_tax_label")
    TOTAL_LABEL = (By.CLASS_NAME, "summary_total_label")
    FINISH_BUTTON = (By.ID, "finish")
    CANCEL_BUTTON = (By.ID, "cancel")

    def is_loaded(self):
        return "checkout-step-two.html" in self.current_url()

    def get_cart_item_count(self):
        return len(self.find_all(self.CART_ITEMS))

    def get_subtotal(self):
        text = self.get_text(self.ITEM_TOTAL)
        return float(text.replace("Item total: $", ""))

    def get_tax(self):
        text = self.get_text(self.TAX_LABEL)
        return float(text.replace("Tax: $", ""))

    def get_total(self):
        text = self.get_text(self.TOTAL_LABEL)
        return float(text.replace("Total: $", ""))

    def finish(self):
        element = self.find(self.FINISH_BUTTON)
        self.driver.execute_script("arguments[0].click();", element)
        time.sleep(1)
        return self

    def cancel(self):
        element = self.find(self.CANCEL_BUTTON)
        self.driver.execute_script("arguments[0].click();", element)
        time.sleep(0.5)
        return self