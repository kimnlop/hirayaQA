import os
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from helpers import Helpers


class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)  # Reuse a single WebDriverWait instance

        # Locators
        self.locators = {
            "username": (By.NAME, "username"),
            "password": (By.NAME, "password"),
            "remember_me": (By.ID, "rememberMe"),
            "show_password": (By.XPATH, "//button[@aria-label='Show password']"),
            "hide_password": (By.XPATH, "//button[@aria-label='Hide password']"),
            "login_button": (By.XPATH, "//button[@type='submit']"),
            "unknown_device_message": (By.XPATH, "//h3[contains(text(), 'Unknown Device')]"),
        }

    def enter_text(self, field_name, text):
        """Generic method to enter text into an input field."""
        try:
            field = self.wait.until(EC.presence_of_element_located(self.locators[field_name]))
            assert field.is_displayed(), f"{field_name} field is not visible!"
            field.clear()  # Clear input before entering text
            field.send_keys(text)
            assert field.get_attribute("value") == text, f"Failed to enter text in {field_name}!"
            print(f"✅ Entered '{text}' in {field_name}")
        except Exception as e:
            print(f"❌ Error entering text in {field_name}: {e}")

    def click_element(self, element_name, description):
        """Generic method to click an element."""
        try:
            element = self.wait.until(EC.element_to_be_clickable(self.locators[element_name]))
            assert element.is_displayed(), f"{description} is not visible!"
            element.click()
            print(f"✅ Clicked {description}")
        except Exception as e:
            print(f"❌ Error clicking {description}: {e}")

    def enter_username(self, username):
        self.enter_text("username", username)

    def enter_password(self, password):
        self.enter_text("password", password)

    def toggle_remember_me(self):
        self.click_element("remember_me", "Remember Me checkbox")

    def toggle_password_visibility(self):
        self.click_element("show_password", "Show Password button")
        self.click_element("hide_password", "Hide Password button")

    def click_login(self):
        self.click_element("login_button", "Login button")

    def is_unknown_device_message_displayed(self):
        """Check if the 'Unknown Device' message is displayed."""
        try:
            return self.wait.until(EC.presence_of_element_located(self.locators["unknown_device_message"])).is_displayed()
        except Exception:
            return False


class TestLoginPage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Initialize WebDriver once for all tests to improve efficiency."""
        Helpers.close_existing_chrome_sessions()

        chrome_options = Options()
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        chrome_options.add_argument("--log-level=3")

        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.implicitly_wait(10)
        cls.driver.get("https://www.himo.bems.hirayatech.ai/")
        cls.login_page = LoginPage(cls.driver)
        cls.helper = Helpers(cls.driver)

    def test_login(self):
        """Test login functionality with Remember Me and password visibility toggling."""
        print("\nStarting login test...")

        username = os.getenv("HIMO_USERNAME", "kimqsantos")
        password = os.getenv("HIMO_PASSWORD", "hiraya@7827")

        self.login_page.enter_username(username)
        self.login_page.enter_password(password)
        self.login_page.toggle_remember_me()
        self.login_page.toggle_password_visibility()
        self.login_page.click_login()

        unknown_device_displayed = self.login_page.is_unknown_device_message_displayed()
        print("✅ 'Unknown Device' message displayed" if unknown_device_displayed else "❌ 'Unknown Device' message NOT found.")

        self.assertTrue(unknown_device_displayed, "❌ Login failed: 'Unknown Device' text not found.")

    @classmethod
    def tearDownClass(cls):
        """Close the browser session after all tests."""
        cls.helper.tearDown()
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()
