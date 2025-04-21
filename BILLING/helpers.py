from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import psutil
import os
import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


class Helpers:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def login(self, username=None, password=None):
        """Reusable login method (No MFA) with dropdown theme toggle"""
        username = username or os.getenv("HIMO_USERNAME", "kimqsantos")
        password = password or os.getenv("HIMO_PASSWORD", "hiraya@7827")

        try:
            try:
                toggle_button = self.wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(@class, 'rounded-full') and contains(@class, 'cursor-pointer')]")
                ))
                toggle_button.click()
                print("✅ Theme toggle opened")

                dark_option = self.wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//div[@role='menuitem' and text()='Light']")
                ))
                dark_option.click()
                print("Light mode selected")

                time.sleep(0.5)

                toggle_button.click()
                print("✅ Theme toggle opened again")

                light_option = self.wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//div[@role='menuitem' and text()='Dark']")
                ))
                light_option.click()
                print("Dark mode selected")

                time.sleep(0.5)

            except Exception as theme_error:
                print(f"Theme toggle failed: {theme_error}")

            # ✅ Login Fields
            username_field = self.wait.until(EC.visibility_of_element_located((By.NAME, "username")))
            username_field.clear()
            username_field.send_keys(username)
            print(f"✅ Username entered: {username}")

            password_field = self.wait.until(EC.visibility_of_element_located((By.NAME, "password")))
            password_field.clear()
            password_field.send_keys(password)
            print("✅ Password entered")

            remember_me = self.wait.until(EC.element_to_be_clickable((By.ID, "rememberMe")))
            if not remember_me.is_selected():
                remember_me.click()
                print("✅ Remember Me checkbox checked")
                remember_me.click() 
                print("✅ Remember Me checkbox checked again")
            else:
                print("Remember Me checkbox was already checked")

            login_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
            login_button.click()
            print("✅ Login button clicked")

            himoBilling = self.wait.until(EC.visibility_of_element_located((
                By.XPATH, "//*[@id='root']/div[1]/div/div[1]/div[2]/div/div[1]/ul/li/a/div[2]/span"
            )))
            assert himoBilling.is_displayed(), "HIMO Billing text not found after login"
            print("✅ HIMO Billing text found")

            print("✅ Login successful (No MFA)")

        except Exception as e:
            print(f"❌ Login failed: {e}")


    def logout(self):
        """Reusable logout method"""
        try:
            user_menu = self.wait.until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, 'span.truncate.text-xs')
            ))

            # Find the parent button element based on the span location (using By.XPATH)
            user_menu_button = user_menu.find_element(By.XPATH, 'ancestor::button')

            # Click the user menu
            user_menu_button.click()
            print("User menu clicked.")

            logout_item = self.wait.until(EC.element_to_be_clickable((
                By.XPATH,
                "//div[@role='menuitem' and normalize-space()='Log out']"
            )))
            logout_item.click()
            print("✅ Logout item clicked")
            
            time.sleep(2)
            self.wait.until(EC.visibility_of_element_located((By.NAME, "username")))
            print("✅ Logout successful")

        except Exception as e:
            print(f"❌ Logout failed: {e}")

    def checkSidebarItems(self):
        """Asserts that sidebar items are present on the page after login and prints them"""
        try:
            sidebar_list = self.wait.until(EC.presence_of_element_located((
                By.XPATH, "//*[@id='root']/div[1]/div/div[1]/div[2]/div/div[2]/div/div/ul"
            )))
            sidebar_items = sidebar_list.find_elements(By.TAG_NAME, "li")

            assert len(sidebar_items) > 0, "❌ No sidebar items found"
            print(f"✅ Sidebar loaded with {len(sidebar_items)} item(s):")

            for i, item in enumerate(sidebar_items, 1):
                text = item.text.strip()
                print(f"  {i}. {text if text else '[No text]'}")

        except Exception as e:
            print(f"❌ Sidebar assertion failed: {e}")

    def clickSelectedItem(self, label):
        """Clicks a sidebar item by partial text match (case-insensitive)"""
        try:
            sidebar_list = self.wait.until(EC.presence_of_element_located((
                By.XPATH, "//*[@id='root']/div[1]/div/div[1]/div[2]/div/div[2]/div/div/ul"
            )))
            sidebar_items = sidebar_list.find_elements(By.TAG_NAME, "li")

            for item in sidebar_items:
                text = item.text.strip()
                if label.lower() in text.lower():
                    item.click()
                    print(f"\n✅ Clicked sidebar item: {text}")
                    return

            raise Exception(f"Sidebar item with label '{label}' not found")

        except Exception as e:
            print(f"❌ Failed to click sidebar item: {e}")
