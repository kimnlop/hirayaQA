import os
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


class TestReportPage(unittest.TestCase):
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

    def test_reportPage(self):
        print("\nStarting Report Page test...")
        self.helper.login()
        self.helper.checkSidebarItems()
        self.helper.clickSelectedItem("Reports")
        self.checkReportsTabList()
        self.checkPaymentsTab()
        self.checkPaymentsTabButtons()
        self.checkTableColumnSorting()
        self.checkSearchBar()
        self.checkWeeklyPaymentsTab()
        self.checkWeeklyPaymentsChart()
        self.checkRecentPendingTable()
        self.driver.back()
        self.helper.logout()
        self.driver.quit()

    def checkReportsTabList(self):
        print("\n📋 Checking Reports tab list...")

        try:
            tablist = self.driver.find_element(By.XPATH, "//div[@role='tablist']")
            tab_buttons = tablist.find_elements(By.XPATH, ".//button[@role='tab']")

            if not tab_buttons:
                print("❌ No tab buttons found.")
                return

            print(f"✅ Found {len(tab_buttons)} tab(s):")
            for i, tab in enumerate(tab_buttons, 1):
                print(f"  {i}. {tab.text.strip()}")

        except Exception as e:
            print(f"❌ Failed to retrieve report tabs: {e}")
    
    def checkPaymentsTab(self):
        print("\n📋 Checking Payments tab...")

        try:
            tablist = self.driver.find_element(By.XPATH, "//div[@role='tablist']")
            tabs = tablist.find_elements(By.XPATH, ".//button[@role='tab']")

            payments_tab = None

            for tab in tabs:
                if tab.text.strip().lower() == "payments":
                    payments_tab = tab
                    break

            if not payments_tab:
                print("❌ Payments tab not found.")
                return

            payments_tab.click()
            print("✅ Payments tab clicked.")

            time.sleep(2)

            active_tab = self.driver.find_element(By.XPATH, "//button[@role='tab' and @aria-selected='true']")
            if "Payments" in active_tab.text:
                print("✅ Payments tab is active.")
            else:
                print(f"❌ Expected 'Payments', but active tab is: {active_tab.text.strip()}")

        except Exception as e:
            print(f"❌ Failed to check Payments tab: {e}")

    def checkPaymentsTabButtons(self):
        print("\n🔘 Checking Payments tab action buttons...")

        try:
            wait = WebDriverWait(self.driver, 10)

            # Show X rows button
            show_rows_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(., 'Show') and contains(., 'rows')]")))
            print("✅ 'Show X rows' button is visible.")
            self.driver.execute_script("arguments[0].click();", show_rows_button)  
            print("✅ Clicked 'Show X rows' button.")

            # Date Picker button
            date_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[@id='date' and contains(., '-') and contains(., '2025')]")))
            print("✅ Date Picker button is visible.")
            date_button.click()
            print("✅ Clicked Date Picker button.")

            # Filter button
            filter_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(., 'Filter') and @type='button']")))
            print("✅ Filter button is visible.")
            filter_button.click()
            print("✅ Clicked Filter button.")

            # Export button
            export_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(., 'Export')]")))
            print("✅ Export button is visible.")
            export_button.click()
            print("✅ Clicked Export button.")

            time.sleep(1)

            # Click file type dropdown
            filetype_dropdown = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[@role='combobox']")))
            print("✅ File type dropdown is visible.")
            filetype_dropdown.click()
            time.sleep(0.5)

            # Select the first available file type option
            filetype_option = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//div[@role='option']")))
            selected_file_type = filetype_option.text
            filetype_option.click()
            print(f"✅ Selected file type: {selected_file_type}")

            time.sleep(1)

            # Confirm Export
            confirm_export_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="radix-:r1h:"]/div/div[3]/button[2]')))
            print("✅ Export confirmation button is visible.")

            # # Take snapshot of files before export
            # download_dir = "C:/Users/kimqs/Downloads"
            # before_download = set(os.listdir(download_dir))

            # Click export confirm button
            confirm_export_button.click()
            print("✅ Confirmed export.")

            # Click Cancel button to close export modal (if still open)
            try:
                cancel_button = wait.until(EC.element_to_be_clickable((
                    By.XPATH, "//button[text()='Cancel']"
                )))
                cancel_button.click()

            except Exception as e:
                print(f"⚠️ Could not click 'Cancel' button (maybe already closed): {e}")

            # file_downloaded = False
            # for _ in range(10):  # Polling for 10 seconds max
            #     time.sleep(1)
            #     after_download = set(os.listdir(download_dir))
            #     new_files = list(after_download - before_download)
            #     if new_files:
            #         # Optional: filter only Excel files
            #         new_excel_files = [f for f in new_files if f.endswith(".json")]
            #         if new_excel_files:
            #             print(f"✅ File downloaded: {new_excel_files[0]}")
            #             file_downloaded = True
            #             break

            # if not file_downloaded:
            #     print("❌ No export file found in download folder.")


        except TimeoutException as te:
            print(f"❌ Timed out waiting for a button: {te}")
        except Exception as e:
            print(f"❌ Failed to check Payments tab buttons: {e}")

    def checkSearchBar(self):
        try:
            wait = WebDriverWait(self.driver, 10)

            search_input = wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='Search consumer...']"))
            )

            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", search_input)
            search_input.click()
            time.sleep(0.3)

            # Clear the input first (if needed)
            search_input.clear()

            gibberish = "zxcasdqwe123"
            for char in gibberish:
                search_input.send_keys(char)
                time.sleep(0.1) 

            time.sleep(1.5) 

            # Wait for "No results." to appear
            no_results = wait.until(
                EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'No results.')]"))
            )

            print("\n✅ Search bar works — 'No results.' is displayed after typing non-existent entry.")

        except Exception as e:
            print("❌ Search bar test failed:", str(e))


    def checkTableColumnSorting(self):
        print("\n➡️ Checking and clicking table column headers to sort...")

        try:
            wait = WebDriverWait(self.driver, 10)
            headers = wait.until(EC.presence_of_all_elements_located((
                By.XPATH, "//table//th//button[./span]"
            )))

            print(f"🔢 Found {len(headers)} column headers.")

            actions = ActionChains(self.driver)

            for index, header in enumerate(headers):
                column_name = header.text.strip()
                print(f"\n➡️ Column {index + 1}: '{column_name}'")

                # Close any open menu by pressing ESC
                actions.send_keys(Keys.ESCAPE).perform()


                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", header)

                try:
                    header.click()
                    print(f"✅ Clicked to sort '{column_name}' ascending.")
                    time.sleep(1)
                except Exception as e:
                    print(f"❌ Could not click '{column_name}' header: {e}")

        except Exception as e:
            print(f"❌ Failed while checking table columns: {e}")


    def checkWeeklyPaymentsTab(self):
        print("\n📋 Checking Weekly Payments tab...")

        try:
            tablist = self.driver.find_element(By.XPATH, "//div[@role='tablist']")
            tabs = tablist.find_elements(By.XPATH, ".//button[@role='tab']")

            weeklyPayments_tab = None

            for tab in tabs:
                if tab.text.strip().lower() == "weekly payments":
                    weeklyPayments_tab = tab
                    break

            if not weeklyPayments_tab:
                print("❌ Payments tab not found.")
                return

            weeklyPayments_tab.click()
            print("✅ Weekly Payments tab clicked.")

            time.sleep(2)

            active_tab = self.driver.find_element(By.XPATH, "//button[@role='tab' and @aria-selected='true']")
            if "Weekly Payments" in active_tab.text:
                print("✅ Weekly Payments tab is active.")
            else:
                print(f"❌ Expected 'Weekly Payments', but active tab is: {active_tab.text.strip()}")

        except Exception as e:
            print(f"❌ Failed to check Payments tab: {e}")

    def checkWeeklyPaymentsChart(self):
        try:
            wait = WebDriverWait(self.driver, 10)

            chart_header = wait.until(
                EC.visibility_of_element_located((By.XPATH, "//h3[text()='Weekly Payments']"))
            )
            print("✅ Weekly Payments chart header is visible.")

            chart_svg = wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "svg.recharts-surface"))
            )
            print("✅ Weekly Payments chart is visible.")
            
            legend_labels = ["Paid", "Pending"]

            for label in legend_labels:
                try:
                    legend = wait.until(
                        EC.visibility_of_element_located((By.XPATH, f"//div[contains(text(), '{label}')]"))
                    )
                    legend.click()
                    print(f"✅ '{label}' legend is visible and clickable")
                except Exception as e:
                    print(f"❌ '{label}' legend not found or not clickable: {e}")

        except Exception as e:
            self.driver.save_screenshot("chart_debug.png")
            print("❌ Weekly Payments chart test failed. Screenshot saved: chart_debug.png")
            print("Error:", str(e))
            
    def checkRecentPendingTable(self):
        """"Check the Recent Pending table for visibility and content."""
        print("\n📋 Checking Recent Pending table...")
        wait = WebDriverWait(self.driver, 10)

        try:
            header = wait.until(EC.visibility_of_element_located((By.XPATH, "//h3[text()='Recent Pending']")))
            print("✅ 'Recent Pending' header is visible")

            table = wait.until(EC.visibility_of_element_located((By.XPATH, "//table[contains(@class, 'w-full')]")))
            print("✅ Table is visible")

            headers = ["Consumer", "Acc No.", "Amount"]
            for col in headers:
                header_element = wait.until(EC.visibility_of_element_located((By.XPATH, f"//th[contains(text(), '{col}')]")))
                print(f"✅ Column '{col}' is visible")

        except Exception as e:
            print(f"❌ Error while checking Recent Pending table: {e}")

if __name__ == "__main__":
    unittest.main()
