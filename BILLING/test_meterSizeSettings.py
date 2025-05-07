import time
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from helpers import Helpers
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import re

class TestMeterSizePage(unittest.TestCase):
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        new_profile_path = r"C:\Users\kimqs\Desktop\Web Drivers\chrome_profile"
        chrome_options.add_argument(f"user-data-dir={new_profile_path}")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)
        self.driver.get("https://www.himo.billing.hirayatech.ai/login")
        self.helper = Helpers(self.driver)
        self.wait = WebDriverWait(self.driver, 10)

    def test_meterSizeSettings(self):
        print("\nStarting Meter & Connection Settings Page test...")
        self.helper.login()
        self.helper.checkSidebarItems()
        self.helper.clickSelectedItem("Meter & Connection Settings")
        self.clickMeterSize()
        self.helper.checkTable("Meter Size")
        self.helper.logout()
        self.driver.quit()

    
    def clickMeterSize(self):
        try:
            self.helper.clickSubSidebarItem("Meter Size")
            print("Successfully navigated to Meter Size page.")

            # Verify page title
            title = self.wait.until(EC.visibility_of_element_located((
                By.XPATH, "//h1[text()='Meter Size']"
            )))
            assert title.is_displayed(), "Meter Size title is not visible."
            print("✅ Verified page title is visible.")

            # Verify 'Show entry' dropdown is visible
            show_dropdown = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "//button[contains(., 'Show')]"
            )))
            assert show_dropdown.is_displayed(), "'Show entries' dropdown is not visible."
            print("✅ Verified 'Show entries' dropdown is visible.")

            # Input gibberish text into the search field like a real user
            time.sleep(3)
            search_input = self.wait.until(EC.visibility_of_element_located((
                By.XPATH, "//input[@placeholder='Search Meter Size...']"
            )))
            search_input.clear()

            gibberish = "asdasd123@#@#"
            for char in gibberish:
                search_input.send_keys(char)


            print("✅ Gibberish text entered in the search input.")

            # Verify Error Handling if there are no matched entry searched
            no_result_text = self.wait.until(EC.visibility_of_element_located((
                By.XPATH, "//td[text()='No results.']")))
            assert no_result_text.is_displayed(), "No Results Text is not visible."
            print("✅ 'No results' text is visible" )
            time.sleep(1.5)
            for char in gibberish:
                search_input.send_keys(Keys.BACK_SPACE)



            # Add Meter Size
            add_meter_button = self.wait.until(EC.visibility_of_element_located(( 
                By.XPATH, "//*[@id='root']/div[1]/div/div[3]/div/div/div/div[1]/div[2]/main/div/button")))
            add_meter_button.click()

            add_meter_header = self.wait.until(EC.visibility_of_element_located((
                By.XPATH, "//div[@role='dialog']//h1[text()='Add Meter Size']")))
            assert add_meter_header.is_displayed(), "Add Meter Modal Header is not visible"
            print("✅ Add Meter Modal Header is visible")
            
            # Verify Modal Components
            connection_type_text = self.wait.until(EC.visibility_of_element_located((
                By.XPATH, "//label[contains(., 'Connection type')]"
            )))
            assert connection_type_text.is_displayed(), "'Connection type' is not visible"
            print("✅ Connection type is visible")

            size_text = self.wait.until(EC.visibility_of_element_located((
                By.XPATH, "//label[contains(., 'Size')]")))
            assert size_text.is_displayed(), "Size is not visible"
            print("✅ Size is visible")

            description_text = self.wait.until(EC.visibility_of_element_located((
                By.XPATH, "//label[contains(., 'Description')]")))
            assert description_text.is_displayed(), "Description is not visible"
            print("✅ Description is visible")

                # Click connection type drop down
            connection_type_dropwdown = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "//button[contains(., 'Select a connection type')]"
            )))
            connection_type_dropwdown.click()
            print("✅ Opened connection type dropdown.")

                # Select "Resindential" option
            resedential_option = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "//div[@role='option' and contains(., 'Residential')]"
            )))
            resedential_option.click()
            print("✅ Selected 'Residential' as connection type.")

                # Size input field
            size_input_field = self.wait.until(EC.visibility_of_element_located((
                By.XPATH, "//input[@placeholder='Input size']"
            )))
            size_input_field.clear()

            size_text = "25"
            for char in size_text:
                size_input_field.send_keys(char)
            print("'25' typed in the size input field")


                # Description input field
            description_input_field = self.wait.until(EC.visibility_of_element_located((
                By.ID, "textarea"
            )))
            description_input_field.clear()

            description_test_text = "Sample Description Text"
            for char in description_test_text:
                description_input_field.send_keys(char)
            print("'Sample Description Text' typed in the description input field")

                # Click Add
            confirm_add_button = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "//button[normalize-space(text())='Add']")))
            confirm_add_button.click()

                # Confirmation toast
            toast = self.wait.until(EC.visibility_of_element_located((
                By.XPATH,
                "//li[@role='status' and @data-state='open']//div[contains(text(), 'Added Meter Size Successfully')]"
            )))

            assert toast.is_displayed(), "❌ Toast message is not visible!"
            print("✅ Toast message 'Added Meter Size Successfully' is visible.")

            # Delete Entry
            ellipsis_button = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "//span[text()='Open']/.."
            )))
            ActionChains(self.driver).move_to_element(ellipsis_button).click().perform()
            print("✅ Clicked the ellipsis menu button.")

            delete_option = self.wait.until(EC.element_to_be_clickable((
                By.XPATH,
                "//div[@role='menuitem' and contains(text(), 'Delete Meter Size')]"
            )))
            delete_option.click()
            print("🗑️  'Delete Meter Size' option clicked.")

            label_element = self.wait.until(EC.visibility_of_element_located((
                By.XPATH, "//label[contains(text(), 'Type')]"
            )))
            label_text = label_element.text
            print(f"✅ Label found: {label_text}")

            # Step 2: Extract the number using regex
            match = re.search(r'Type\s+"(\d+)"\s+to delete\.', label_text)
            assert match, "❌ Could not find number in label text"
            dynamic_number = match.group(1)
            print(f"✅ Extracted number to delete: {dynamic_number}")

            input_field = self.wait.until(EC.element_to_be_clickable((
                By.ID, label_element.get_attribute("for")
            )))
            input_field.clear()
            input_field.send_keys(dynamic_number)
            print("✅ Entered the dynamic number into the input field.")

            delete_button = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "//button[normalize-space(text())='Delete']")))
            delete_button.click()

        except TimeoutException:
            self.fail("Timeout while performing an action in the Meter and Connection Settings page.")
        except AssertionError as e:
            self.fail(f"Assertion failed: {e}")    