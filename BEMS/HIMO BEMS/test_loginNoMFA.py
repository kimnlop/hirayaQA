import os
import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from helpers import Helpers

class LoginPageNoMFA:
    def __init__(self, driver):
        self.driver = driver
        self.username_input = (By.NAME, "username")
        self.password_input = (By.NAME, "password")
        self.remember_me_checkbox = (By.ID, "rememberMe")
        self.show_password_button = (By.XPATH, "//button[@aria-label='Show password']")
        self.hide_password_button = (By.XPATH, "//button[@aria-label='Hide password']")
        self.login_button = (By.XPATH, "//button[@type='submit']")
        self.himo_overview = (By.XPATH, "//span[contains(text(), 'Overview')]")

    def enter_username(self, username):
        try:
            username_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.username_input)
            )
            assert username_field.is_displayed(), "Username field is not visible!"
            username_field.send_keys(username)
            assert username_field.get_attribute("value") == username, "Username input failed!"
            print(f"✅ Username entered: {username}")
        except Exception as e:
            print(f"❌ Error entering username: {e}")

    def enter_password(self, password):
        try:
            password_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.password_input)
            )
            assert password_field.is_displayed(), "Password field is not visible!"
            password_field.send_keys(password)
            print("✅ Password entered")  
        except Exception as e:
            print(f"❌ Error entering password: {e}")

    def toggle_remember_me(self):
        try:
            remember_me_checkbox = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.remember_me_checkbox)
            )
            assert remember_me_checkbox.is_displayed(), "Remember Me checkbox is not visible!"
            if not remember_me_checkbox.is_selected():
                remember_me_checkbox.click()
                print("✅ Remember Me checkbox checked")
            else:
                print("Remember Me checkbox was already checked")
        except Exception as e:
            print(f"❌ Error toggling Remember Me checkbox: {e}")

    def toggle_password_visibility(self):
        try:
            show_password_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.show_password_button)
            )
            assert show_password_button.is_displayed(), "Show Password button is not visible!"
            show_password_button.click()

            hide_password_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.hide_password_button)
            )
            assert hide_password_button.is_displayed(), "Hide Password button is not visible!"
            hide_password_button.click()

            print("✅ Password visibility toggled")
        except Exception as e:
            print(f"❌ Error toggling password visibility: {e}")

    def click_login(self):
        try:
            login_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.login_button)
            )
            assert login_button.is_displayed(), "Login button is not visible!"
            login_button.click()
            time.sleep(2)  # Allow page to load
        except Exception as e:
            print(f"❌ Error clicking login button: {e}")

    def verify_overview(self):
        try:
            overview_text = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.himo_overview)
            )
            assert overview_text.is_displayed(), "Overview text not found!"
            print("✅ Overview text displayed")
        except Exception as e:
            print(f"❌ Error verifying overview text: {e}")

class SidebarPage:
    def __init__(self, driver, helper):
        self.driver = driver
        self.helper = helper
        self.sidebar_buttons = self.helper.sidebar_elements  

    def verify_sidebar_options(self):
        """Verify all sidebar buttons are present and click them."""
        try:
            for button_name, locator in self.sidebar_buttons.items():
                button = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located(locator)
                )
                assert button.is_displayed(), f"❌ {button_name} button is not visible!"
                print(f"✅ {button_name} button is visible in the sidebar")

                button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(locator)
                )
                button.click()
                print(f"✅ Clicked on the {button_name} button")
        except Exception as e:
            print(f"❌ Error verifying or clicking sidebar buttons: {e}")

# Test Class
class TestLoginPageNoMFA(unittest.TestCase):
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        new_profile_path = r"C:\Users\kimqs\Desktop\Web Drivers\chrome_profile"
        chrome_options.add_argument(f"user-data-dir={new_profile_path}")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)
        self.driver.get("https://www.himo.bems.hirayatech.ai/")
        self.helper = Helpers(self.driver)  # ✅ Fixed reference

        # ✅ Initialize Page Objects
        self.login_page_no_mfa = LoginPageNoMFA(self.driver)
        self.sidebar_page = SidebarPage(self.driver, self.helper)  # ✅ Pass helper here

    def test_login_no_mfa(self):
        print("\nStarting login test (No MFA)...")
        username = os.getenv("HIMO_USERNAME", "kimqsantos")  
        password = os.getenv("HIMO_PASSWORD", "hiraya@7827")  

        self.login_page_no_mfa.enter_username(username)
        self.login_page_no_mfa.enter_password(password)
        self.login_page_no_mfa.toggle_remember_me()
        self.login_page_no_mfa.toggle_password_visibility()
        self.login_page_no_mfa.click_login()
        self.login_page_no_mfa.verify_overview()
        self.sidebar_page.verify_sidebar_options()

        self.helper.logout()

    def tearDown(self):
        """Closes the browser after each test."""
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
