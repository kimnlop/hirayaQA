import time
import unittest
import os
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from helpers import Helpers  

class TestWaterManagementPage(unittest.TestCase):
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        profile_path = r"C:\\Users\\kimqs\\OneDrive\\Desktop\\Web Drivers\\chrome_profile"
        chrome_options.add_argument(f"user-data-dir={profile_path}")

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)
        self.driver.get("https://www.himo.bems.hirayatech.ai/")   
        self.helper = Helpers(self.driver)

        # Login
        username = os.getenv("HIMO_USERNAME", "kimqsantos")
        password = os.getenv("HIMO_PASSWORD", "hiraya@7827")
        self.helper.perform_login(username, password)

        # Element Dictionary
        self.element = {
            "Water Level Graph": {
                "Water Level Title": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[1]/div[1]/div[1]"),
                "Download CSV": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[1]/div[1]/div[2]/button[2]"),
                "Graph": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[1]/div[2]/div/div/div/*[name()='svg']"),
                "Label": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[1]/div[2]/div/div/div/div[1]/div/div"),
            },
        }
    
    def test_water_management_page(self):
        print("\nStarting Water Management Page Test...")
        self.helper.verify_page("Water Management")
        self.verify_water_level_graph()
        self.extract_pumps()
        self.helper.logout()
        self.helper.tearDown()

    def _verify_element(self, name, locator):
        """Helper method to verify element visibility."""
        try:
            element = WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located(locator))
            assert element.is_displayed(), f"❌ '{name}' is not visible!"
            print(f"✅ {name} is visible")
        except Exception as e:
            print(f"❌ Error verifying '{name}': {str(e)}")

    def verify_water_level_graph(self):
        """Verify Water Levels Graph Components"""
        print("\nChecking Water Level Graph")
        for element_name, locator in self.element["Water Level Graph"].items():
            self._verify_element(element_name, locator)
    
    def extract_pumps(self):
        """Extracts all available pumps and their metrics, clicks the button, and returns to the main page."""
        print(f"\nVerifying pumps...")

        try:
            pumps = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'rounded-lg border bg-card text-card-foreground')]")

            if not pumps:
                print("❌ No pumps found!")
                return

            for i, pump in enumerate(pumps):
                try:
                    # Re-find the pumps in case the DOM is refreshed after navigation
                    pumps = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'rounded-lg border bg-card text-card-foreground')]")
                    pump = pumps[i]  # Access the pump again

                    pump_name = pump.find_element(By.XPATH, ".//h3").text.strip()
                    print(f"\n🔹 Pump: {pump_name}")

                    metrics = {
                        metric.find_element(By.XPATH, "./span").text.strip().replace(":", ""): metric.text.split(":")[1].strip()
                        for metric in pump.find_elements(By.XPATH, ".//p")
                        if ":" in metric.text
                    }

                    for key, value in metrics.items():
                        print(f"    {key}: {value}")

                    try:
                        # Click the "Stop Pump" button if available
                        status_button = pump.find_element(By.XPATH, ".//button[contains(text(), 'Stop Pump')]")
                        print(f"    ✅ Clicking 'Stop Pump' for {pump_name}")
                        status_button.click()
                        self.driver.implicitly_wait(3)  # Wait for action to complete

                        # Navigate back to the main page
                        self.driver.back()
                        self.driver.implicitly_wait(3) 

                    except Exception as e:
                        print(f"    ❌ No 'Stop Pump' button found for {pump_name}: {e}")

                except Exception as e:
                    print(f"❌ Error extracting data for a pump: {e}")

        except Exception as e:
            print(f"❌ Error finding pumps: {e}")

if __name__ == "__main__":
    unittest.main()

# "Water Level" Pump is being detected when extracting the pump section
# No function to verify date filters yet
# No process yet
