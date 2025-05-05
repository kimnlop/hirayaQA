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

# To do error handling for search
# User Billing Info Table entries
# CRUD for adding a billing user in clickBillingUserInfo()


class TestUserRoleManagementPage(unittest.TestCase):
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

    def test_userRoleManagement(self):
        print("\nStarting User & Role Management Page test...")
        self.helper.login()
        self.helper.checkSidebarItems()
        self.helper.clickSelectedItem("User & Role Management")
        self.clickBillingUserInfo()
        self.checkTable("User Billing Info")
        self.clickPosition()
        self.checkTable("Position")
        self.clickDepartment()
        self.checkTable("Department")
        self.helper.logout()
        self.driver.quit()
        
    def clickBillingUserInfo(self):
        try:
            self.helper.clickSubSidebarItem("Billing User Info")
            print("Successfully navigated to Billing User Info page.")

            # Verify page title
            title = self.wait.until(EC.visibility_of_element_located((
                By.XPATH, "//h1[text()='Billing User Info']"
            )))
            assert title.is_displayed(), "Billing User Info title is not visible."
            print("✅ Verified page title is visible.")

            # Verify 'Show entry' dropdown is visible
            show_dropdown = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "//button[contains(., 'Show')]"
            )))
            assert show_dropdown.is_displayed(), "'Show entries' dropdown is not visible."
            print("✅ Verified 'Show entries' dropdown is visible.")

            # Input gibberish text into the search field
            search_input = self.wait.until(EC.visibility_of_element_located((
                By.XPATH, "//input[@placeholder='Search username...']"
            )))
            search_input.clear()
            search_input.send_keys("asdasd123@#@#")
            print("✅ Gibberish text entered in the search input.")

            # Click 'Add Billing User' button (Updated XPath)
            add_button = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, '//*[@id="root"]/div[1]/div/div[3]/main/div/div[1]/div[2]/main/button'
            )))
            add_button.click()
            print("✅ Clicked 'Add Billing User' button.")

            # Verify modal appears with header
            modal_header = self.wait.until(EC.visibility_of_element_located((
                By.XPATH, "//div[@role='dialog']//h1[text()='Add Billing User']"
            )))
            assert modal_header.is_displayed(), "'Add Billing User' modal did not appear."
            print("✅ Verified 'Add Billing User' modal is visible.")

            # Close the modal using the Cancel button
            cancel_button = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "//button[text()='Cancel']"
            )))
            cancel_button.click()
            print("✅ Closed the modal using the 'Cancel' button.")

            # Click the Export button (updated XPath)
            export_button = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, '//*[@id="root"]/div[1]/div/div[3]/main/div/div[1]/div[2]/button'
            )))
            export_button.click()
            print("✅ Clicked the Export button.")

            # Open export type dropdown
            export_type_dropdown = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "//button[contains(., 'Select export type')]"
            )))
            export_type_dropdown.click()
            print("✅ Opened export type dropdown.")

            # Select '.xlsx' file type
            xlsx_option = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "//div[@role='option' and contains(., '.xlsx')]"
            )))
            xlsx_option.click()
            print("✅ Selected '.xlsx' as export type.")

            # Click the Export button for .xlsx
            final_export_button = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "//button[contains(., 'Export') and contains(@class, 'bg-[#00a1a3]')]"
            )))
            final_export_button.click()
            print("✅ Exported '.xlsx' file.")

            # Re-open dropdown to select '.json'
            export_type_dropdown = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "//button[contains(., '.xlsx')]"  # dropdown now shows .xlsx
            )))
            export_type_dropdown.click()
            print("✅ Re-opened export type dropdown.")

            # Select '.json' file type
            json_option = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "//div[@role='option' and contains(., '.json')]"
            )))
            json_option.click()
            print("✅ Selected '.json' as export type.")

            # Click the Export button for .json
            final_export_button = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "//button[contains(., 'Export') and contains(@class, 'bg-[#00a1a3]')]"
            )))
            final_export_button.click()
            print("✅ Exported '.json' file.")

            # Close the export modal by clicking 'Cancel'
            cancel_button = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "//button[text()='Cancel' and contains(@class, 'border-input')]"
            )))
            cancel_button.click()
            print("✅ Closed the export modal using the 'Cancel' button.")

            # Verify the "Filter" button is visible and clickable
            filter_button = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "//button[contains(., 'Filter') and contains(@class, 'border-input')]"
            )))
            assert filter_button.is_displayed(), "❌ Filter button is not visible!"
            print("✅ Filter button is visible and clickable.")

        except TimeoutException:
            self.fail("Timeout while performing an action in the Billing User Info page.")
        except AssertionError as e:
            self.fail(f"Assertion failed: {e}")            

    def checkTable(self, table_name):
        print(f"\n🔍 Checking {table_name} Table Headers...")

        header_buttons = self.wait.until(EC.presence_of_all_elements_located((
            By.XPATH, "//thead//th//button"
        )))

        actions = ActionChains(self.driver)

        for btn in header_buttons:
            header_text = btn.text.strip()
            assert header_text != "", "❌ Found a header with empty text!"
            assert btn.is_displayed(), f"❌ Header '{header_text}' is not visible!"
            assert btn.is_enabled(), f"❌ Header '{header_text}' is not clickable!"

            # Click to test clickability
            btn.click()
            print(f"🔁 Clicked header '{header_text}' once.")
            time.sleep(0.5)

            # Press ESC to close dropdown/popover
            actions.send_keys(Keys.ESCAPE).perform()
            time.sleep(0.2)

            print(f"✅ Header '{header_text}' passed click test and dropdown closed.")

        try:
            actions_header = self.driver.find_element(By.XPATH, "//thead//th/div[text()='Actions']")
            assert actions_header.is_displayed(), "❌ 'Actions' header not visible!"
            print("✅ Header 'Actions' is visible")
        except Exception:
            print("⚠️ 'Actions' header not found or not visible.")

        print(f"✅ {table_name} Table header check complete.")


    def clickPosition(self):
        try:
            self.helper.clickSubSidebarItem("Position")
            print("Successfully navigated to Position page.")

            # Verify page title
            title = self.wait.until(EC.visibility_of_element_located((
                By.XPATH, "//h1[text()='Position']"
            )))
            assert title.is_displayed(), "Position title is not visible."
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
                By.XPATH, "//input[@placeholder='Search Departments...']"
            )))
            search_input.clear()

            gibberish = "asdasd123@#@#"
            for char in gibberish:
                search_input.send_keys(char)
                time.sleep(0.1)  

            print("✅ Gibberish text entered in the search input.")

            # Click 'Position' button (Updated XPath)
            add_button = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, '//*[@id="root"]/div[1]/div/div[3]/div/div/div[1]/div[2]/main/button'
            )))
            add_button.click()
            print("✅ Clicked 'Position' button.")

            # Verify modal appears with updated header text
            modal_header = self.wait.until(EC.visibility_of_element_located((
                By.XPATH, "//h1[contains(@class, 'text-3xl') and contains(text(), 'Add Position')]"
            )))
            assert modal_header.is_displayed(), "'Add Position' modal did not appear."
            print("✅ Verified 'Add Position' modal is visible.")

            # Close the modal using the updated Cancel button style
            cancel_button = self.wait.until(EC.element_to_be_clickable(( 
                By.XPATH, "//button[contains(@class, 'border border-input') and text()='Cancel']"
            )))
            cancel_button.click()
            print("✅ Closed the modal using the updated 'Cancel' button.")

            # Click the Export button (updated XPath)
            export_button = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, '//*[@id="root"]/div[1]/div/div[3]/div/div/div[1]/div[2]/button'
            )))
            export_button.click()
            print("✅ Clicked the Export button.")

            # Open export type dropdown
            export_type_dropdown = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "//button[contains(., 'Select export type')]"
            )))
            export_type_dropdown.click()
            print("✅ Opened export type dropdown.")

            # Select '.xlsx' file type
            xlsx_option = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "//div[@role='option' and contains(., '.xlsx')]"
            )))
            xlsx_option.click()
            print("✅ Selected '.xlsx' as export type.")

            # Click the Export button for .xlsx
            final_export_button = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "//button[contains(., 'Export') and contains(@class, 'bg-[#00a1a3]')]"
            )))
            final_export_button.click()
            print("✅ Exported '.xlsx' file.")

            # Re-open dropdown to select '.json'
            export_type_dropdown = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "//button[contains(., '.xlsx')]"  # dropdown now shows .xlsx
            )))
            export_type_dropdown.click()
            print("✅ Re-opened export type dropdown.")

            # Select '.json' file type
            json_option = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "//div[@role='option' and contains(., '.json')]"
            )))
            json_option.click()
            print("✅ Selected '.json' as export type.")

            # Click the Export button for .json
            final_export_button = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "//button[contains(., 'Export') and contains(@class, 'bg-[#00a1a3]')]"
            )))
            final_export_button.click()
            print("✅ Exported '.json' file.")

            # Close the export modal by clicking 'Cancel'
            cancel_button = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "//button[text()='Cancel' and contains(@class, 'border-input')]"
            )))
            cancel_button.click()
            print("✅ Closed the export modal using the 'Cancel' button.")

            # Verify the "Filter" button is visible and clickable
            filter_button = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "//button[contains(., 'Filter') and contains(@class, 'border-input')]"
            )))
            assert filter_button.is_displayed(), "❌ Filter button is not visible!"
            print("✅ Filter button is visible and clickable.")

        except TimeoutException:
            self.fail("Timeout while performing an action in the Position page.")
        except AssertionError as e:
            self.fail(f"Assertion failed: {e}")    


    def clickDepartment(self):
        try:
            self.helper.clickSubSidebarItem("Department")
            print("Successfully navigated to Department page.")

            # Verify page title
            title = self.wait.until(EC.visibility_of_element_located((
                By.XPATH, "//h1[text()='Department']"
            )))
            assert title.is_displayed(), "Department title is not visible."
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
                By.XPATH, "//input[@placeholder='Search Departments...']"
            )))
            search_input.clear()

            gibberish = "asdasd123@#@#"
            for char in gibberish:
                search_input.send_keys(char)
                time.sleep(0.1)  # Simulate typing delay per character (adjust as needed)

            print("✅ Gibberish text entered in the search input.")

            # Click 'Department' button (Updated XPath)
            add_button = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, '//*[@id="root"]/div[1]/div/div[3]/div/div/div[1]/div[2]/main/button'
            )))
            add_button.click()
            print("✅ Clicked 'Department' button.")

            # Verify modal appears with updated header text
            modal_header = self.wait.until(EC.visibility_of_element_located((
                By.XPATH, "//h1[contains(@class, 'text-3xl') and contains(text(), 'Add Department')]"
            )))
            assert modal_header.is_displayed(), "'Add Department' modal did not appear."
            print("✅ Verified 'Add Department' modal is visible.")

            # Close the modal using the updated Cancel button style
            cancel_button = self.wait.until(EC.element_to_be_clickable(( 
                By.XPATH, "//button[contains(@class, 'border border-input') and text()='Cancel']"
            )))
            cancel_button.click()
            print("✅ Closed the modal using the updated 'Cancel' button.")

            # Click the Export button (updated XPath)
            export_button = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, '//*[@id="root"]/div[1]/div/div[3]/div/div/div[1]/div[2]/button'
            )))
            export_button.click()
            print("✅ Clicked the Export button.")

            # Open export type dropdown
            export_type_dropdown = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "//button[contains(., 'Select export type')]"
            )))
            export_type_dropdown.click()
            print("✅ Opened export type dropdown.")

            # Select '.xlsx' file type
            xlsx_option = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "//div[@role='option' and contains(., '.xlsx')]"
            )))
            xlsx_option.click()
            print("✅ Selected '.xlsx' as export type.")

            # Click the Export button for .xlsx
            final_export_button = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "//button[contains(., 'Export') and contains(@class, 'bg-[#00a1a3]')]"
            )))
            final_export_button.click()
            print("✅ Exported '.xlsx' file.")

            # Re-open dropdown to select '.json'
            export_type_dropdown = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "//button[contains(., '.xlsx')]"  # dropdown now shows .xlsx
            )))
            export_type_dropdown.click()
            print("✅ Re-opened export type dropdown.")

            # Select '.json' file type
            json_option = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "//div[@role='option' and contains(., '.json')]"
            )))
            json_option.click()
            print("✅ Selected '.json' as export type.")

            # Click the Export button for .json
            final_export_button = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "//button[contains(., 'Export') and contains(@class, 'bg-[#00a1a3]')]"
            )))
            final_export_button.click()
            print("✅ Exported '.json' file.")

            # Close the export modal by clicking 'Cancel'
            cancel_button = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "//button[text()='Cancel' and contains(@class, 'border-input')]"
            )))
            cancel_button.click()
            print("✅ Closed the export modal using the 'Cancel' button.")

            # Verify the "Filter" button is visible and clickable
            filter_button = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "//button[contains(., 'Filter') and contains(@class, 'border-input')]"
            )))
            assert filter_button.is_displayed(), "❌ Filter button is not visible!"
            print("✅ Filter button is visible and clickable.")

        except TimeoutException:
            self.fail("Timeout while performing an action in the Department page.")
        except AssertionError as e:
            self.fail(f"Assertion failed: {e}")    
            
if __name__ == "__main__":
    unittest.main()
