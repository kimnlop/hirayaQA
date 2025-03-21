from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import psutil  

class Helpers:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

        # Locators
        self.username_input = (By.NAME, "username")
        self.password_input = (By.NAME, "password")
        self.remember_me_checkbox = (By.ID, "rememberMe")
        self.show_password_button = (By.XPATH, "//button[@aria-label='Show password']")
        self.hide_password_button = (By.XPATH, "//button[@aria-label='Hide password']")
        self.login_button = (By.XPATH, "//button[@type='submit']")
        self.user_menu_button = (By.XPATH, "//button[contains(@class, 'rounded-full') and @aria-haspopup='menu']")
        self.logout_button = (By.XPATH, "//div[contains(text(), 'Logout')]")

        # Sidebar Elements
        sidebar_base_xpath = "//*[@id='root']/div[1]/div/aside/nav[1]/div/a"
        self.sidebar_elements = {
            "Overview": (By.XPATH, f"{sidebar_base_xpath}[1]/*[name()='svg']"),
            "SLD": (By.XPATH, f"{sidebar_base_xpath}[2]/*[name()='svg']"),
            "HVAC": (By.XPATH, f"{sidebar_base_xpath}[3]/*[name()='svg']"),
            "Water Management": (By.XPATH, f"{sidebar_base_xpath}[4]/*[name()='svg']"),
            "Light Control": (By.XPATH, f"{sidebar_base_xpath}[5]/*[name()='svg']"),
            "FDAS": (By.XPATH, f"{sidebar_base_xpath}[6]/*[name()='svg']"),
            "CCTV and Doors": (By.XPATH, f"{sidebar_base_xpath}[7]/*[name()='svg']"),
            "Parking": (By.XPATH, f"{sidebar_base_xpath}[8]/*[name()='svg']"),
            "Battery Monitoring": (By.XPATH, f"{sidebar_base_xpath}[9]/*[name()='svg']"),
            "Elevators Escalator": (By.XPATH, f"{sidebar_base_xpath}[10]/*[name()='svg']"),
            "Power Meters": (By.XPATH, f"{sidebar_base_xpath}[11]/*[name()='svg']"),
            "Public Address": (By.XPATH, f"{sidebar_base_xpath}[12]/*[name()='svg']"),
            "Alarms": (By.XPATH, f"{sidebar_base_xpath}[13]/*[name()='svg']"),
        }

    def find_element(self, locator):
        """Returns a web element if found."""
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_element_and_click(self, locator, error_msg):
        """Finds and clicks an element."""
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
            return True
        except Exception:
            print(f"❌ {error_msg}")
            return False

    def enter_text(self, locator, text, error_msg):
        """Finds an input field and enters text."""
        try:
            field = self.find_element(locator)
            field.clear()
            field.send_keys(text)
            assert field.get_attribute("value") == text, f"Input failed for {text}"
            print(f"✅ Entered {text}")
        except Exception:
            print(f"❌ {error_msg}")

    def enter_username(self, username):
        self.enter_text(self.username_input, username, "Error entering username!")

    def enter_password(self, password):
        self.enter_text(self.password_input, password, "Error entering password!")

    def toggle_remember_me(self):
        """Toggles the Remember Me checkbox."""
        if self.find_element_and_click(self.remember_me_checkbox, "Remember Me checkbox not clickable!"):
            print("✅ Remember Me toggled")

    def toggle_password_visibility(self):
        """Toggles password visibility on and off."""
        if self.find_element_and_click(self.show_password_button, "Show password button not clickable!") and \
           self.find_element_and_click(self.hide_password_button, "Hide password button not clickable!"):
            print("✅ Password visibility toggled")

    def click_login(self):
        """Clicks the login button."""
        if self.find_element_and_click(self.login_button, "Login button not clickable!"):
            print("✅ Login button clicked")
            time.sleep(2)  # Allow page to load

    def verify_page(self, page_name):
        """Verifies and clicks a sidebar page after login."""
        if page_name in self.sidebar_elements:
            if self.find_element_and_click(self.sidebar_elements[page_name], f"{page_name} Button Not Found!"):
                print(f"✅ {page_name} page displayed")
        else:
            print(f"❌ Page '{page_name}' not found in sidebar elements.")

    def logout(self):
        """Logs out the user."""
        if self.find_element_and_click(self.user_menu_button, "User menu button not found!") and \
           self.find_element_and_click(self.logout_button, "Logout button not found!"):
            print("✅ Logout successful")

    def tearDown(self):
        """Closes the browser."""
        print("\nClosing browser...")
        self.driver.quit()

    def perform_login(self, username, password):
        """Performs the full login sequence."""
        self.enter_username(username)
        self.enter_password(password)
        self.toggle_remember_me()
        self.toggle_password_visibility()
        self.click_login()

    def extract_equipment_data(self):
        """Extracts all available equipment within rooms and their metrics."""
        print(f"Verifying equipment...")

        try:
            rooms = self.driver.find_elements(By.XPATH, "//div[@class='space-y-2']")
            if not rooms:
                print("❌ No rooms found!")
                return

            for room in rooms:
                try:
                    room_name = room.find_element(By.XPATH, ".//h2").text.strip()
                    print(f"\nRoom: {room_name}")

                    equipment_list = room.find_elements(By.XPATH, ".//div[contains(@class, 'rounded-lg border bg-card')]")
                    if not equipment_list:
                        print(f"No equipment found in {room_name}.")
                        continue

                    for device in equipment_list:
                        try:
                            device_name = device.find_element(By.XPATH, ".//label").text.strip()
                            status_element = device.find_element(By.XPATH, ".//button[@role='switch']")
                            device_status = "ON" if status_element.get_attribute("aria-checked") == "true" else "OFF"

                            # Extract all available metrics
                            metrics = {
                                metric.text.split(":")[0].strip(): metric.text.split(":")[1].strip()
                                for metric in device.find_elements(By.XPATH, ".//div[contains(@class, 'text-muted-foreground')]")
                                if ":" in metric.text
                            }

                            print(f"⚙️  Device: {device_name}, Status: {device_status}")
                            for key, value in metrics.items():
                                print(f"    {key}: {value}")

                        except Exception:
                            print(f"❌ Error extracting data for a device in {room_name}")

                except Exception:
                    print(f"❌ Error extracting data for room!")

        except Exception:
            print(f"❌ Error finding rooms!")

    @staticmethod
    def close_existing_chrome_sessions():
        """Close any existing Chrome browser processes."""
        for process in psutil.process_iter(attrs=['pid', 'name']):
            if "chrome" in process.info['name'].lower():
                try:
                    print(f"Closing existing Chrome process: {process.info['pid']}")
                    psutil.Process(process.info['pid']).terminate()
                except Exception as e:
                    print(f"Error terminating process {process.info['pid']}: {e}")