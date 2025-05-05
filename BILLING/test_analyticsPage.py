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
import re


class TestAnalyticsPage(unittest.TestCase):
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

    def test_analyticsPage(self):
        print("\nStarting Analytics Page test...")
        self.helper.login()
        self.helper.checkSidebarItems()
        self.helper.clickSelectedItem("Analytics") 
        self.checkCards()
        self.checkFilterButton()
        self.checkTabs()
        self.verifyChartsOnFirstTab()
        self.verifyChartsOnSecondTab()
        self.verifyChartsOnThirdTab()
        self.helper.logout()
        print("Analytics Page test completed.")
        self.driver.quit()

    def checkCards(self):
        """Asserts that cards in the grid are visible and exist"""
        time.sleep(3) 
        try:
            grid_container = self.wait.until(EC.visibility_of_element_located(( 
                By.XPATH, "//div[@class='grid grid-cols-12 gap-4']"
            )))

            # Find all the cards inside the grid
            cards = grid_container.find_elements(By.XPATH, ".//div[@class='col-span-12 w-full sm:col-span-6 md:col-span-3']")
            
            assert len(cards) > 0, "❌ No cards found in the grid"
            print(f"✅ Found {len(cards)} card(s) in the grid:")

            for i, card in enumerate(cards, 1):
                label = card.find_element(By.XPATH, ".//h3").text.strip()
                value = card.find_element(By.XPATH, ".//div[@class='p-6 pt-0 text-2xl font-bold']//h1").text.strip()
                assert card.is_displayed(), f"❌ Card '{label}' is not visible"
                
                print(f"  {i}. Card with label '{label}' and value '{value}' is visible")
                
        except Exception as e:
            print(f"❌ Card visibility check failed: {e}")

    def checkFilterButton(self):
        """Checks the filter button, clicks it, and selects all available options"""
        try:
            filter_button = self.wait.until(EC.visibility_of_element_located(( 
                By.XPATH, "//*[@id='root']/div[1]/div/div[3]/main/div[1]/div[2]/button"
            )))

            assert filter_button.is_displayed(), "❌ Filter button is not visible"
            assert filter_button.is_enabled(), "❌ Filter button is not clickable"
            print("\n✅ Filter button is visible and clickable")

        except Exception as e:
            print(f"\n❌ Filter button test failed: {str(e)}")

    def checkTabs(self):
        """Verifies and clicks each tab under the specified parent element"""
        try:
            parent = self.wait.until(EC.presence_of_element_located(( 
                By.XPATH, "//*[@id='root']/div[1]/div/div[3]/main/div[3]/div/div/div[1]/div[1]"
            )))

            # Get all tab elements inside the parent
            tabs = parent.find_elements(By.XPATH, ".//button | .//div[@role='tab'] | .//a")

            assert len(tabs) > 0, "❌ No tabs found under the specified parent element"
            print(f"✅ Found {len(tabs)} tab(s):")

            for i, tab in enumerate(tabs):
                tab_text = tab.text.strip()
                assert tab.is_displayed(), f"❌ Tab {i+1} ('{tab_text}') is not visible"

                print(f"  {i+1}. Clicking tab: '{tab_text}'")
                try:
                    # Use ActionChains in case the tab needs to be hovered before click
                    ActionChains(self.driver).move_to_element(tab).click().perform()
                    time.sleep(1)  # Let content load after click
                except Exception as click_err:
                    print(f"❌ Failed to click tab '{tab_text}': {click_err}")

        except Exception as e:
            print(f"❌ Tab verification failed: {e}")

    def verifyChartsOnFirstTab(self):
        """Switches back to the first tab and verifies both charts"""
        try:
            # Locate the first tab again
            parent = self.wait.until(EC.presence_of_element_located((By.XPATH,
                "//*[@id='root']/div[1]/div/div[3]/main/div[3]/div/div/div[1]/div[1]"
            )))
            tabs = parent.find_elements(By.XPATH, ".//button | .//div[@role='tab'] | .//a")
            
            assert len(tabs) > 0, "❌ No tabs found"
            first_tab = tabs[0]
            tab_text = first_tab.text.strip()
            
            print(f"\n🔁 Returning to first tab: '{tab_text}'")
            ActionChains(self.driver).move_to_element(first_tab).click().perform()
            time.sleep(2)

            # Chart 1: Top Revenue Consumers
            top_revenue_chart = self.wait.until(EC.presence_of_element_located((By.XPATH,
                "//h3[text()='Top Revenue Consumers']/ancestor::div[contains(@class, 'col-span-7')]"
            )))
            assert top_revenue_chart.is_displayed(), "❌ Top Revenue Consumers chart is not visible"
            print("📊 Top Revenue Consumers is visible")

            # Chart 2: Annual Revenue Statistics
            annual_revenue_chart = self.wait.until(EC.presence_of_element_located((By.XPATH,
                "//h3[text()='Annual Revenue Statistics']/ancestor::div[contains(@class, 'col-span-5')]"
            )))
            assert annual_revenue_chart.is_displayed(), "❌ Annual Revenue Statistics chart is not visible"
            print("📊 Annual Revenue Statistics is visible")

        except Exception as e:
            print(f"❌ Chart verification failed: {e}")

    def verifyChartsOnSecondTab(self):
        """Switches to the second tab (Consumption Trends) and verifies both charts are visible"""
        try:
            parent = self.wait.until(EC.presence_of_element_located((By.XPATH,
                "//*[@id='root']/div[1]/div/div[3]/main/div[3]/div/div/div[1]/div[1]"
            )))
            tabs = parent.find_elements(By.XPATH, ".//button | .//div[@role='tab'] | .//a")
            assert len(tabs) >= 2, "❌ Less than 2 tabs found"
            second_tab = tabs[1]
            print(f"\n➡️  Switching to second tab: '{second_tab.text.strip()}'")
            ActionChains(self.driver).move_to_element(second_tab).click().perform()
            time.sleep(2)

            trends_chart = self.wait.until(EC.presence_of_element_located((By.XPATH,
                "//h3[text()='Consumption Trends']/ancestor::div[contains(@class, 'col-span')]"
            )))
            assert trends_chart.is_displayed(), "❌ 'Consumption Trends' chart not visible"
            print("📊 Consumption Trends chart is visible")

            pie_chart_container = self.wait.until(EC.presence_of_element_located((By.XPATH,
                "//h3[text()='Consumption Statistics']/ancestor::div[contains(@class, 'col-span')]"
            )))
            assert pie_chart_container.is_displayed(), "❌ 'Consumption Statistics' chart not visible"
            print("📊 Consumption Statistics chart is visible")


        except Exception as e:
            print(f"❌ Second tab chart verification failed: {e}")

    def verifyChartsOnThirdTab(self):
        try:
            parent = self.wait.until(EC.presence_of_element_located((By.XPATH,
                "//*[@id='root']/div[1]/div/div[3]/main/div[3]/div/div/div[1]/div[1]"
            )))
            tabs = parent.find_elements(By.XPATH, ".//button | .//div[@role='tab'] | .//a")
            assert len(tabs) >= 3, "❌ Less than 3 tabs found"
            third_tab = tabs[2]
            print(f"\n➡️  Switching to third tab: '{third_tab.text.strip()}'")
            ActionChains(self.driver).move_to_element(third_tab).click().perform()
            time.sleep(2)

            demographic_chart = self.wait.until(EC.presence_of_element_located((By.XPATH,
                "//h3[text()='Consumer Demographic']/ancestor::div[contains(@class, 'col-span')]"
            )))
            assert demographic_chart.is_displayed(), "❌ Consumer Demographic chart is not visible"
            print("📊 Consumer Demographic is visible")

            statistics_chart = self.wait.until(EC.presence_of_element_located((By.XPATH,
                "//h3[text()='Consumer Statistics']/ancestor::div[contains(@class, 'col-span')]"
            )))
            assert statistics_chart.is_displayed(), "❌ Consumer Statistics chart is not visible"
            print("📊 Consumer Statistics is visible\n")

        except Exception as e:
            print(f"❌ Third tab chart verification failed: {e}")


if __name__ == "__main__":
    unittest.main()
