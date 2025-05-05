import os
import time
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from helpers import Helpers
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class TestLandingPage(unittest.TestCase):
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        new_profile_path = r"C:\Users\ASUS\Desktop\Web Drivers\chrome_profile"
        chrome_options.add_argument(f"user-data-dir={new_profile_path}")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)
        self.driver.get("https://www.himo.billing.hirayatech.ai/login")
        self.helper = Helpers(self.driver)
        self.wait = WebDriverWait(self.driver, 10)

    def test_login(self):
        print("\nStarting Landing Page test...")
        self.helper.login()
        self.checkLoggedInUser()
        self.checkMenuItems()
        self.isUserMatched()
        self.helper.logout()
        self.driver.quit()

    def checkLoggedInUser(self):
        try:
            user_menu = self.wait.until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, 'span.truncate.text-xs')
            ))
            user_menu_button = user_menu.find_element(By.XPATH, 'ancestor::button')

            # Click the user menu
            user_menu_button.click()
            print("User menu clicked.")

            self.logged_in_name = self.wait.until(EC.visibility_of_element_located((
                By.XPATH, "//div[@class='grid flex-1 text-left text-sm leading-tight']/span[1]"))).text.strip()
            
            self.logged_in_email = self.wait.until(EC.visibility_of_element_located((
                By.XPATH, "//div[@class='grid flex-1 text-left text-sm leading-tight']/span[2]"))).text.strip()

            print(f"✅ Logged-in user: {self.logged_in_name}, Email: {self.logged_in_email}")

        except Exception as e:
            print(f"❌ Error verifying logged-in user: {e}")

    def checkMenuItems(self):
        try:
            menu_items = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, "//*[@role='menuitem']")))
            
            print("\n📋 Available menu items:")
            for index, item in enumerate(menu_items, start=1):
                item_name = item.text.strip()
                print(f"{index}. {item_name}")

        except Exception as e:
            print(f"❌ Error retrieving menu items: {e}")

    def isUserMatched(self):
        print("\nChecking if the user matches the profile page...")
        profile_menu_item = self.wait.until(EC.element_to_be_clickable((
            By.XPATH, "//*[@role='menuitem' and contains(text(), 'Profile')]")))
        profile_menu_item.click()
        try:
            profile_name = self.wait.until(EC.visibility_of_element_located((
                By.XPATH, "//h2[@class='text-3xl font-bold tracking-tight']"))).text.strip()
            
            profile_email = self.wait.until(EC.visibility_of_element_located((
                By.XPATH, "//p[text()='Email']/following-sibling::p"))).text.strip()

            print(f"Profile page name: {profile_name}")
            print(f"Profile page email: {profile_email}")

            name_match = self.logged_in_name.lower() == profile_name.lower()
            email_match = self.logged_in_email.lower() == profile_email.lower()

            if name_match and email_match:
                print("✅ User name and email match the profile page.")
                return True
            else:
                print("❌ Mismatch found:")
                if not name_match:
                    print(f"   - Name: expected '{self.logged_in_name}', found '{profile_name}'")
                if not email_match:
                    print(f"   - Email: expected '{self.logged_in_email}', found '{profile_email}'")
                return False
            
        except Exception as e:
            print(f"❌ Error verifying user match: {e}")
            return False
        
        


if __name__ == "__main__":
    unittest.main()
