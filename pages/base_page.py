from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def load_url(self, url):
        self.driver.get(url)

    def current_url(self):
        return self.driver.current_url

    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_all(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type_text(self, locator, text):
        # NOTE: do not use element.clear() here. saucedemo's checkout form
        # fields are React-controlled inputs, and Selenium's native clear()
        # does not reliably fire the 'input' event React listens for - the
        # field can end up visually/DOM-wise empty even though clear()
        # "succeeded". Select-all + Delete does fire real keyboard events,
        # so React's state stays in sync with what's on screen.
        element = self.find(locator)
        element.click()
        element.send_keys(Keys.CONTROL, "a")
        element.send_keys(Keys.DELETE)
        element.send_keys(text)

    def get_text(self, locator):
        return self.find(locator).text

    def is_visible(self, locator):
        try:
            return self.wait.until(EC.visibility_of_element_located(locator)).is_displayed()
        except Exception:
            return False

    def wait_for_url_contains(self, fragment):
        """Explicit wait replacement for time.sleep() after navigation clicks."""
        return self.wait.until(EC.url_contains(fragment))

    def is_present(self, locator):
        """Like is_visible but doesn't require the element to be on-screen/displayed."""
        try:
            self.wait.until(EC.presence_of_element_located(locator))
            return True
        except Exception:
            return False