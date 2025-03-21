import time
import unittest
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from helpers import Helpers  
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestSLDPage(unittest.TestCase):
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        profile_path = r"C:\Users\kimqs\OneDrive\Desktop\Web Drivers\chrome_profile"
        chrome_options.add_argument(f"user-data-dir={profile_path}")

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)
        self.driver.get("https://www.himo.bems.hirayatech.ai/")
        self.helpers = Helpers(self.driver)  

        # Login
        username = os.getenv("HIMO_USERNAME", "kimqsantos")
        password = os.getenv("HIMO_PASSWORD", "hiraya@7827")
        self.helpers.perform_login(username, password)

        # Element dictionary using tuple format
        self.elements = {
            "Diagram": {
                "graph": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[1]/div/div[2]"),
                "Circuit Button": {
                    "DS Button": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[1]/div/div[2]/div[2]/div[2]/div[1]/*[name()='svg']"),
                    "PCB Button": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[1]/div/div[2]/div[3]/div[2]/div[1]/*[name()='svg']"),
                    "10 MVA Button": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[1]/div/div[2]/div[4]/div[2]/div[1]/*[name()='svg']"),
                    "MAIN Button": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[1]/div/div[2]/div[5]/div[2]/div[1]/*[name()='svg']"),
                    "Button 5": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[1]/div/div[2]/div[6]/div[2]/div[1]/div[1]/div[2]/*[name()='svg']"),
                    "Button 6": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[1]/div/div[2]/div[6]/div[2]/div[1]/div[2]/div[2]/*[name()='svg']"),
                    "Button 7": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[1]/div/div[2]/div[6]/div[2]/div[1]/div[3]/div[2]/*[name()='svg']"),
                    "Button 8": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[1]/div/div[2]/div[6]/div[2]/div[1]/div[4]/div[2]/*[name()='svg']"),
                    "Button 9": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[1]/div/div[2]/div[6]/div[2]/div[1]/div[5]/div[2]/*[name()='svg']"),
                    "Button 10": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[1]/div/div[2]/div[6]/div[2]/div[2]/div[2]/*[name()='svg']"),
                },
            },
            "Power Meters" : {
                "title" : (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[2]/div/div/div/h1"),
                "meters" : {
                    "Power Meter 1" : {
                        "title" : (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[2]/div/div/div/div/div[1]/div[1]/h3"),
                        "meter" : (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[2]/div/div/div/div/div[1]/div[2]/div/*[name()='svg']")
                    },
                    "Power Meter 2" : {
                        "title" : (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[2]/div/div/div/div/div[2]/div[1]/h3"),
                        "meter" : (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[2]/div/div/div/div/div[2]/div[2]/div/*[name()='svg']")
                    },
                    "Power Meter 3" : {
                        "title" : (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[2]/div/div/div/div/div[3]/div[1]/h3"),
                        "meter" : (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[2]/div/div/div/div/div[3]/div[2]/div/*[name()='svg']")
                    },
                    "Power Meter 4" : {
                        "title" : (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[2]/div/div/div/div/div[4]/div[1]/h3"),
                        "meter" : (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[2]/div/div/div/div/div[4]/div[2]/div/*[name()='svg']")
                    },
                    "Power Meter 5" : {
                        "title" : (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[2]/div/div/div/div/div[5]/div[1]/h3"),
                        "meter" : (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[2]/div/div/div/div/div[5]/div[2]/div/*[name()='svg']")
                    },
                    "Power Meter 6" : {
                        "title" : (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[2]/div/div/div/div/div[6]/div[1]/h3"),
                        "meter" : (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[2]/div/div/div/div/div[6]/div[2]/div/*[name()='svg']")
                    },
                }
            },
        }
        

    def test_SLD_page(self):
        print("\nStarting SLD Page Test...")
        self.helpers.verify_page("SLD")
        self.verify_diagram()
        self.verify_power_meters()

        # Logout
        self.helpers.logout()
        self.helpers.tearDown()
    
    def verify_element(self, category, element_name, subcategory=None):
        """General function to verify if an element is visible."""
        try:
            # Retrieve element locator
            if subcategory:
                element_locator = self.elements[category][subcategory].get(element_name)
            else:
                element_locator = self.elements[category].get(element_name)

            if not element_locator:
                raise ValueError(f"❌ '{element_name}' not found in '{category}' dictionary.")

            # Wait for element to be visible
            element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(element_locator)
            )
            assert element.is_displayed(), f"❌ '{element_name}' is not visible!"
            print(f"✅ '{element_name}' is visible")
            return element
        except Exception as e:
            print(f"❌ Error verifying '{element_name}': {e}")
            return None

    def verify_diagram(self):
        """Verify SL Diagram and Click Circuit Buttons with Confirmation"""

        print("\nStarting Diagram Test...")

        # Verify and check if SL Diagram is displayed
        diagram_element = self.verify_element("Diagram", "graph")
        if diagram_element:
            print("✅ SL Diagram is displayed correctly!")
        else:
            print("❌ SL Diagram is NOT displayed.")
            return

        try:
            for button_name, button_xpath in self.elements["Diagram"]["Circuit Button"].items():
                # Click Circuit Button
                circuit_button = self.verify_element("Diagram", button_name, subcategory="Circuit Button")
                if circuit_button:
                    circuit_button.click()
                    print(f"✅ {button_name} clicked successfully!")

                    # Click any available "Yes" confirmation button
                    try:
                        confirmation_button = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, "//button[text()='Yes']"))
                        )
                        confirmation_button.click()
                        print("✅ Confirmation button clicked!")
                    except Exception:
                        print("⚠ No confirmation button found or already clicked.")

        except Exception as e:
            print(f"❌ Error clicking buttons: {e}")

    def verify_power_meters(self):
        """Verify all power meters are visible and clickable."""
        print("\nVerifying power meters...")

        try:
            # Verify Power Meters title
            power_meters_title = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.elements["Power Meters"]["title"])
            )
            assert power_meters_title.is_displayed(), "❌ Power Meters title not found!"
            print("✅ Power Meters title is visible")

            # Verify each power meter
            for meter_name, meter_info in self.elements["Power Meters"]["meters"].items():
                meter_title = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located(meter_info["title"])
                )
                print(f"\nPower Meter {meter_name}")
                assert meter_title.is_displayed(), f"❌ {meter_name} title not found!"
                print(f"✅ {meter_name} title is visible")

                meter_icon = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(meter_info["meter"])
                )
                assert meter_icon.is_displayed(), f"❌ {meter_name} meter icon not found!"
                print(f"✅ {meter_name} is visible")
                meter_icon.click()
                print(f"✅ {meter_name} is clicked")
                self.driver.back()

        except Exception as e:
            print(f"❌ Error verifying power meters: {e}")
      

if __name__ == "__main__":
    unittest.main()
