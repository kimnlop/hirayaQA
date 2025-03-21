import os
import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class LoginPageNoMFA:
    def __init__(self, driver):
        self.driver = driver
        self.username_input = (By.NAME, "username")
        self.password_input = (By.NAME, "password")
        self.remember_me_checkbox = (By.ID, "rememberMe")
        self.show_password_button = (By.XPATH, "//button[@aria-label='Show password']")
        self.hide_password_button = (By.XPATH, "//button[@aria-label='Hide password']")
        self.login_button = (By.XPATH, "//button[@type='submit']")
        self.unknown_device_message = (By.XPATH, "//h3[contains(text(), 'Unknown Device')]")
        self.himo_boilerplate_text = (By.XPATH, "//span[contains(text(), 'HIMO Boilerplate')]")
    
    def enter_username(self, username):
        try:
            usernameField = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.username_input))
            assert usernameField.is_displayed(), "Username field is not visible!"
            usernameField.send_keys(username)
            assert usernameField.get_attribute("value") == username, "Username input failed!"
            print(f"✅ Username entered: {username}")
        except Exception as e:
            print(f"❌ Error entering username: {e}")
        
    def enter_password(self, password):
        try:
            passwordField = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.password_input))  
            assert passwordField.is_displayed(), "Password field is not visible!"
            passwordField.send_keys(password)
            assert passwordField.get_attribute("value") == password, "Password input failed!"
            print("✅ Password entered") 
        except Exception as e: 
            print(f"❌ Error entering password: {e}")
        
    def toggle_remember_me(self):
        try:
            rememberMeCheckbox = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.remember_me_checkbox))
            assert rememberMeCheckbox.is_displayed(), "Remember Me checkbox is not visible!"
            if not rememberMeCheckbox.is_selected():
                rememberMeCheckbox.click()
                print("✅ Remember Me checkbox checked")
            else:
                print("ℹ️ Remember Me checkbox was already checked")
        except Exception as e:
            print(f"❌ Error toggling Remember Me checkbox: {e}")
    
    def toggle_password_visibility(self):
        try:
            showPasswordButton = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.show_password_button))
            assert showPasswordButton.is_displayed(), "Show Password button is not visible!"
            showPasswordButton.click()
            
            hidePasswordButton = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.hide_password_button))
            assert hidePasswordButton.is_displayed(), "Hide Password button is not visible!"
            hidePasswordButton.click()
            
            print("✅ Password visibility toggled")
        except Exception as e:
            print(f"❌ Error toggling password visibility: {e}")
        
    def click_login(self):
        try:
            loginButton = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.login_button))
            assert loginButton.is_displayed(), "Login button is not visible!"
            loginButton.click()
        except Exception as e:
            print(f"❌ Error clicking login button: {e}")
    
    def verify_himo_boilerplate_text(self):
        try:
            himoBoilerplateText = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.himo_boilerplate_text))
            assert himoBoilerplateText.is_displayed(), "HIMO Boilerplate text is not visible!"
            print("✅ HIMO Boilerplate text displayed")
        except Exception as e:
            print(f"❌ Error verifying HIMO Boilerplate text: {e}")

# Test Class
class TestLoginPageNoMFA(unittest.TestCase):
    def setUp(self):  # ✅ Corrected from "setup" to "setUp"
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        new_profile_path = r"C:\Users\kimsa\OneDrive\Desktop\Selenium Test\chrome_profile"
        chrome_options.add_argument(f"user-data-dir={new_profile_path}")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)
        self.driver.get("http://localhost:5173/login")
        self.login_page_no_mfa = LoginPageNoMFA(self.driver)  # Initialize login page object
    

    def test_login_no_mfa(self):
        print("\n🔄 Starting login test (No MFA)...")
        self.login_page_no_mfa.enter_username("kimqsantos")
        self.login_page_no_mfa.enter_password("hiraya@7827")
        self.login_page_no_mfa.toggle_remember_me()
        self.login_page_no_mfa.toggle_password_visibility()
        self.login_page_no_mfa.click_login()
        self.login_page_no_mfa.verify_himo_boilerplate_text()
        

        
if __name__ == "__main__":
    unittest.main()
