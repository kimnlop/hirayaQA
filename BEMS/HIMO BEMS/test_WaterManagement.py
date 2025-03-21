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
        profile_path = r"C:\Users\kimqs\OneDrive\Desktop\Web Drivers\chrome_profile"
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

        }

    def test_battery_monitoring_page(self):
        print("\nStarting Water Management Page Test...")
        self.helper.verify_page("Water Management")

        self.helper.logout()
        self.helper.tearDown()
        

    
 

if __name__ == "__main__":
    unittest.main()