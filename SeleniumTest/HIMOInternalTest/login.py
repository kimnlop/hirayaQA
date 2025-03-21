import os
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configure Chrome WebDriver path
os.environ['PATH'] += r';C:\Users\kimsa\OneDrive\Desktop\Selenium Test\chromedriver-win64'

# Page Object Model (POM) for Login Page
class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.username_input = (By.NAME, "username")
        self.password_input = (By.NAME, "password")
        self.remember_me_checkbox = (By.ID, "rememberMe")
        self.show_password_button = (By.XPATH, "//button[@aria-label='Show password']")
        self.hide_password_button = (By.XPATH, "//button[@aria-label='Hide password']")
        self.login_button = (By.XPATH, "//button[@type='submit']")
        self.unknown_device_message = (By.XPATH, "//h3[contains(text(), 'Unknown Device')]")

    def enter_username(self, username):
        try:
            field = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.username_input))
            assert field.is_displayed(), "Username field is not visible!"
            field.send_keys(username)
            assert field.get_attribute("value") == username, "Username input failed!"
            print(f"✅ Username entered: {username}")
        except Exception as e:
            print(f"❌ Error entering username: {e}")

    def enter_password(self, password):
        try:
            field = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.password_input))
            assert field.is_displayed(), "Password field is not visible!"
            field.send_keys(password)
            assert field.get_attribute("value") == password, "Password input failed!"
            print("✅ Password entered")
        except Exception as e:
            print(f"❌ Error entering password: {e}")

    def toggle_remember_me(self):
        try:
            checkbox = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.remember_me_checkbox))
            assert checkbox.is_displayed(), "Remember Me checkbox is not visible!"
            if not checkbox.is_selected():
                checkbox.click()
                print("✅ Remember Me checkbox checked")
            else:
                print("ℹ️ Remember Me checkbox was already checked")
        except Exception as e:
            print(f"❌ Error toggling Remember Me checkbox: {e}")

    def toggle_password_visibility(self):
        try:
            show_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.show_password_button))
            assert show_button.is_displayed(), "Show Password button is not visible!"
            show_button.click()
            
            hide_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.hide_password_button))
            assert hide_button.is_displayed(), "Hide Password button is not visible!"
            hide_button.click()
            
            print("✅ Password visibility toggled")
        except Exception as e:
            print(f"❌ Error toggling password visibility: {e}")

    def click_login(self):
        try:
            button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.login_button))
            assert button.is_displayed(), "Login button is not visible!"
            button.click()
            print("✅ Login button clicked")
        except Exception as e:
            print(f"❌ Error clicking login button: {e}")

    def is_unknown_device_message_displayed(self):
        try:
            return WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.unknown_device_message)).is_displayed()
        except Exception:
            return False  # Return False instead of raising an error

# Test Case Using `unittest`
class TestLoginPage(unittest.TestCase):

    def setUp(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        chrome_options.add_argument("--log-level=3")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)
        self.driver.get("http://localhost:5173/login")
        self.login_page = LoginPage(self.driver)

    def test_login(self):
        print("\n🔄 Starting login test...")
        self.login_page.enter_username("kimqsantos")
        self.login_page.enter_password("hiraya@7827")
        self.login_page.toggle_remember_me()
        self.login_page.toggle_password_visibility()
        self.login_page.click_login()

        if self.login_page.is_unknown_device_message_displayed():
            print("✅ 'Unknown Device' message displayed")
        else:
            print("❌ 'Unknown Device' message NOT found.")

        self.assertTrue(self.login_page.is_unknown_device_message_displayed(), "❌ Login failed: 'Unknown Device' text not found.")



# Run the tests
if __name__ == "__main__":
    unittest.main()
