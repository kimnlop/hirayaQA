import time
import unittest
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from helpers import Helpers  

class TestHVACPage(unittest.TestCase):
    def setUp(self):
        Helpers.close_existing_chrome_sessions()
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        profile_path = r"C:\Users\kimqs\OneDrive\Desktop\Web Drivers\chrome_profile"
        chrome_options.add_argument(f"user-data-dir={profile_path}")

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)
        self.driver.get("https://www.himo.bems.hirayatech.ai/")
        self.login_helper = Helpers(self.driver)
    
        # Login
        username = os.getenv("HIMO_USERNAME", "kimqsantos")
        password = os.getenv("HIMO_PASSWORD", "hiraya@7827")
        self.login_helper.perform_login(username, password)

        # Element Dictionary
        self.elements = {
            "building": {
                "Calamba Building": {
                    "title": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/div/div[1]/div/div[1]/h1"),
                    "floors": {
                        "Ground Floor": {
                            "title": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/div/div[1]/div/div[1]/div[2]"),
                        },
                        "First Floor": {
                            "title": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/div/div[1]/div/div[1]/div[3]"),
                        },
                        "Second Floor": {
                            "title": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/div/div[1]/div/div[1]/div[4]"),
                        },
                        "Third Floor": {
                            "title": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/div/div[1]/div/div[1]/div[5]"),
                        },
                        "Fourth Floor": {
                            "title": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/div/div[1]/div/div[1]/div[6]"),
                        },
                    }
                },
                "Calamba Side Building": {
                    "title": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/div/div[1]/div/div[2]/h1"),
                    "floors": {
                        "Ground Floor": {
                            "title": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/div/div[1]/div/div[2]/div[2]"),
                        },
                        "First Floor": {
                            "title": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/div/div[1]/div/div[2]/div[3]"),
                        },
                    }
                }
            }
        }

    def test_HVAC_page(self):
        print("\nStarting HVAC Page Test...")
        self.helper = Helpers(self.driver)
        self.helper.verify_page("HVAC")
        self.verify_buildings()
        self.helper.extract_equipment_data()
        self.helper.logout()
        self.helper.tearDown()

    def _verify_element(self, name, data):
        """Helper method to verify element visibility."""
        try:
            element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(data["title"]))
            assert element.is_displayed(), f"❌ '{name}' is not visible!"
            print(f"✅ {name} is visible")
        except Exception as e:
            print(f"❌ Error verifying '{name}': {e}")
    
    def verify_buildings(self):
        """Verify buildings and dynamically extract equipment data."""
        print("\nChecking Buildings...")

        for building, data in self.elements["building"].items():
            print(f"\nChecking {building} components")
            if "floors" in data:
                for floor, floor_data in data["floors"].items():
                    print(f"\nChecking {floor} components")
                    self._verify_element(floor, floor_data)
                    floors = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(floor_data["title"]))
                    floors.click()
                    print(f"✅ {floor} is clicked")
                    self.helper.extract_equipment_data()
    

if __name__ == "__main__":
    unittest.main()
