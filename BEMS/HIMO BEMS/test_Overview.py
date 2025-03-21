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

class TestOverviewPage(unittest.TestCase):
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        profile_path = r"C:\Users\kimqs\OneDrive\Desktop\Web Drivers\chrome_profile"
        chrome_options.add_argument(f"user-data-dir={profile_path}")

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)
        self.driver.get("https://www.himo.bems.hirayatech.ai/")
        self.helpers = Helpers(self.driver)  

        # Element Dictionary
        self.elements = {
            "sidebar_buttons": {
            "Overview": (By.XPATH, "//a[contains(@class, 'active') and span[text()='Overview']]")
            },
            "power_meters": {
                "Power": {
                    "title": (By.XPATH, "//h3[@class='tracking-tight text-sm font-medium' and text()='Power']"),
                    "gauge": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[1]/div[1]/div[2]"),
                    "kWh": (By.XPATH, "//p[@class='text-xs text-muted-foreground' and text()='kWh']")
                },
                "Water": {
                    "title": (By.XPATH, "//h3[@class='tracking-tight text-sm font-medium' and text()='Water']"),
                    "gauge": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[1]/div[2]/div[2]"),
                    "liters": (By.XPATH, "//p[@class='text-xs text-muted-foreground' and text()='liters']")
                },
                "Gas": {
                    "title": (By.XPATH, "//h3[@class='tracking-tight text-sm font-medium' and text()='Gas']"),
                    "gauge": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[1]/div[3]/div[2]"),
                    "cubic meters (Gas)": (By.XPATH, "//p[@class='text-xs text-muted-foreground' and text()='cubic meters']")
                },
                "Air": {
                    "title": (By.XPATH, "//h3[@class='tracking-tight text-sm font-medium' and text()='Air']"),
                    "gauge": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[1]/div[4]/div[2]"),
                    "cubic meters (Air)": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[1]/div[4]/div[2]/p")
                },
                "Light": {
                    "title": (By.XPATH, "//h3[@class='tracking-tight text-sm font-medium' and text()='Light']"),
                    "gauge": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[1]/div[5]/div[2]"),
                    "watts": (By.XPATH, "//p[@class='text-xs text-muted-foreground' and text()='watts']")
                }
            },
            "buildings": {
                "Calamba Building": (By.XPATH, "//h3[@class='text-2xl font-semibold leading-none tracking-tight' and text()='Calamba Building']"),
                "Calamba Side Building": (By.XPATH, "//h3[@class='text-2xl font-semibold leading-none tracking-tight' and text()='Calamba Side Building']")
                },
            "line_graphs": {
            "Calamba Building": {
                "Power": {
                    "title": (By.XPATH, "//p[@class='block text-lg font-medium capitalize' and text()='power']"),
                    "graph": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[2]/div[2]/div/div[1]/div/div/div/div/*[name()='svg']/*[name()='g'][2]/*[name()='g']"),
                    "labels": {
                        "Current Consumption": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[2]/div[2]/div/div[1]/div/div/div/div/div[1]/div/div[1]"),
                        "Voltage": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[2]/div[2]/div/div[1]/div/div/div/div/div[1]/div/div[2]"),
                        "Current" : (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[2]/div[2]/div/div[1]/div/div/div/div/div[1]/div/div[3]"),
                        "Energy Consumption": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[2]/div[2]/div/div[1]/div/div/div/div/div[1]/div/div[4]"),
                        "Power Factor": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[2]/div[2]/div/div[1]/div/div/div/div/div[1]/div/div[5]"),
                    }
                },
                "Water": {
                    "title": (By.XPATH, "//p[@class='block text-lg font-medium capitalize' and text()='water']"),
                    "graph": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[2]/div[2]/div/div[2]/div/div/div/div/*[name()='svg']/*[name()='g'][2]/*[name()='g']"),
                    "labels": {
                        "Current Flow Rate" : (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[2]/div[2]/div/div[2]/div/div/div/div/div[1]/div/div[1]"),
                        "Total Usage": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[2]/div[2]/div/div[2]/div/div/div/div/div[1]/div/div[2]"),
                        "Pressure": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[2]/div[2]/div/div[2]/div/div/div/div/div[1]/div/div[3]"),
                        "Temperature": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[2]/div[2]/div/div[2]/div/div/div/div/div[1]/div/div[4]"),
                    }
                },
                "Gas": {
                    "title": (By.XPATH, "//p[@class='block text-lg font-medium capitalize' and text()='gas']"),
                    "graph": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[2]/div[2]/div/div[3]/div/div/div/div/*[name()='svg']/*[name()='g'][2]/*[name()='g']"),
                    "labels": {
                        "Current Flow Rate" : (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[2]/div[2]/div/div[3]/div/div/div/div/div[1]/div/div[1]"),
                        "Total Usage": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[2]/div[2]/div/div[3]/div/div/div/div/div[1]/div/div[2]"),
                        "Pressure": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[2]/div[2]/div/div[3]/div/div/div/div/div[1]/div/div[3]"),
                        "Temperature": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[2]/div[2]/div/div[3]/div/div/div/div/div[1]/div/div[4]"),
                    }
                },
                "Air": {
                    "title": (By.XPATH, "//p[@class='block text-lg font-medium capitalize' and text()='air']"),
                    "graph": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[2]/div[2]/div/div[4]/div/div/div/div/*[name()='svg']/*[name()='g'][2]/*[name()='g']"),
                    "labels" : {
                        "Current Comnsumption" : (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[2]/div[2]/div/div[4]/div/div/div/div/div[1]/div/div[1]"),
                        "Temperature" : (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[2]/div[2]/div/div[4]/div/div/div/div/div[1]/div/div[2]"),
                        "Humidity" : (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[2]/div[2]/div/div[4]/div/div/div/div/div[1]/div/div[3]"),
                        "Air Quality" : (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[2]/div[2]/div/div[4]/div/div/div/div/div[1]/div/div[4]"),
                        "Flow Rate" : (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[2]/div[2]/div/div[4]/div/div/div/div/div[1]/div/div[5]"),

                    }
                },
                "Light": {
                    "title": (By.XPATH, "//p[@class='block text-lg font-medium capitalize' and text()='light']"),
                    "graph": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[2]/div[2]/div/div[5]/div/div/div/div/*[name()='svg']/*[name()='g'][2]/*[name()='g']"),
                    "labels" : {
                        "Current Comnsumption" : (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[2]/div[2]/div/div[5]/div/div/div/div/div[1]/div/div[1]"),
                        "Luminosity" : (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[2]/div[2]/div/div[5]/div/div/div/div/div[1]/div/div[2]"),
                        "Energy Comnsumption" : (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[2]/div[2]/div/div[5]/div/div/div/div/div[1]/div/div[3]"),
                    }
                },
                "FDAS": {
                    "title": (By.XPATH, "//p[@class='block text-lg font-medium capitalize' and text()='fdas']"),
                    "graph": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[2]/div[2]/div/div[6]/div/div/div/div/*[name()='svg']/*[name()='g'][2]/*[name()='g']"),
                    "labels" : {
                        "Battery Level" : (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[2]/div[2]/div/div[6]/div/div/div/div/div[1]/div/div")
                    } 
                }
            },
            "Calamba Side Building": {
                "Power": {
                    "title": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[3]/div[2]/div/div[1]/p"),
                    "graph": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[3]/div[2]/div/div[1]/div/div/div/div/*[name()='svg']/*[name()='g'][2]/*[name()='g']"),
                    "labels": {
                        "Current Consumption": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[3]/div[2]/div/div[1]/div/div/div/div/div[1]/div/div[1]"),
                        "Voltage": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[3]/div[2]/div/div[1]/div/div/div/div/div[1]/div/div[2]"),
                        "Current" : (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[3]/div[2]/div/div[1]/div/div/div/div/div[1]/div/div[3]"),
                        "Energy Consumption": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[3]/div[2]/div/div[1]/div/div/div/div/div[1]/div/div[4]"),
                        "Power Factor": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[3]/div[2]/div/div[1]/div/div/div/div/div[1]/div/div[5]"),
                    },
                },
                "Water": {
                    "title": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[3]/div[2]/div/div[2]/p"),
                    "graph": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[3]/div[2]/div/div[2]/div/div/div/div/*[name()='svg']/*[name()='g'][2]/*[name()='g']"),
                    "labels": {
                        "Current Flow Rate" : (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[3]/div[2]/div/div[2]/div/div/div/div/div[1]/div/div[1]"),
                        "Total Usage": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[3]/div[2]/div/div[2]/div/div/div/div/div[1]/div/div[2]"),
                        "Pressure": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[3]/div[2]/div/div[2]/div/div/div/div/div[1]/div/div[3]"),
                        "Temperature": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[3]/div[2]/div/div[2]/div/div/div/div/div[1]/div/div[4]"),
                }
                },
                "Gas": {
                    "title": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[3]/div[2]/div/div[3]/p"),
                    "graph": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[3]/div[2]/div/div[3]/div/div/div/div/*[name()='svg']/*[name()='g'][2]/*[name()='g']"),
                    "labels": {
                        "Current Flow Rate": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[3]/div[2]/div/div[3]/div/div/div/div/div[1]/div/div[1]"),
                        "Total Usage": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[3]/div[2]/div/div[3]/div/div/div/div/div[1]/div/div[2]"),
                        "Pressure": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[3]/div[2]/div/div[3]/div/div/div/div/div[1]/div/div[3]"),
                        "Temperature": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[3]/div[2]/div/div[3]/div/div/div/div/div[1]/div/div[4]"),
                    }
                },
                "Air": {
                    "title": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[3]/div[2]/div/div[4]/p"),
                    "graph": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[3]/div[2]/div/div[4]/div/div/div/div/*[name()='svg']/*[name()='g'][2]/*[name()='g']"),
                    "labels": {
                        "Current Consumption": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[3]/div[2]/div/div[4]/div/div/div/div/div[1]/div/div[1]"),
                        "Temperature": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[3]/div[2]/div/div[4]/div/div/div/div/div[1]/div/div[2]"),
                        "Humidity": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[3]/div[2]/div/div[4]/div/div/div/div/div[1]/div/div[3]"),
                        "Air Quality": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[3]/div[2]/div/div[4]/div/div/div/div/div[1]/div/div[4]"),
                        "Flow Rate": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[3]/div[2]/div/div[4]/div/div/div/div/div[1]/div/div[5]"),
                    }
                },
                "Light": {
                    "title" : (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[3]/div[2]/div/div[5]/p"),
                    "graph": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[3]/div[2]/div/div[5]/div/div/div/div/*[name()='svg']/*[name()='g'][2]/*[name()='g']"),
                    "labels": {
                        "Current Consumption": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[3]/div[2]/div/div[5]/div/div/div/div/div[1]/div/div[1]"),
                        "Luminosity": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[3]/div[2]/div/div[5]/div/div/div/div/div[1]/div/div[2]"),
                        "Energy Consumption": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[3]/div[2]/div/div[5]/div/div/div/div/div[1]/div/div[3]"),
                    }
                },
                "FDAS": {
                    "title" : (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[3]/div[2]/div/div[6]/p"),
                    "graph": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[3]/div[2]/div/div[6]/div/div/div/div/*[name()='svg']/*[name()='g'][2]/*[name()='g']"),
                    "labels": {
                        "Battery Level": (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[3]/div[2]/div/div[6]/div/div/div/div/div[1]/div/div")
                    }
                }
                },

            },
            "energy_consumption": {
                "title" : (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[4]/div[1]/div[1]/h3"),
                "graph" : (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[4]/div[2]/div/div/div/*[name()='svg']/*[name()='g'][3]"),
                "labels" : {
                    "Power" : (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[4]/div[2]/div/div/div/div[1]/div/div[1]"),
                    "Water" : (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[4]/div[2]/div/div/div/div[1]/div/div[2]"),
                    "Gas" : (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[4]/div[2]/div/div/div/div[1]/div/div[3]"),
                    "Air" : (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[4]/div[2]/div/div/div/div[1]/div/div[4]"),
                    "Light" : (By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div/main/div[4]/div[2]/div/div/div/div[1]/div/div[5]"),
                },
            },
        }
            
        

    def test_overview_page(self):
        print("\nStarting Overview Page Test...")

        # Login
        username = os.getenv("HIMO_USERNAME", "kimqsantos")
        password = os.getenv("HIMO_PASSWORD", "hiraya@7827")
        self.helper = Helpers(self.driver)
        self.helper.perform_login(username, password)
        self.helper.verify_page("Overview")

        # Verify Sidebar
        self.verify_element("sidebar_buttons", "Overview")

        # Verify Power Meters (Titles, Gauges & Labels)
        self.verify_power_meters()

        # Verify Buildings & Line Graphs
        self.verify_buildings("buildings")
        self.verify_line_graphs()

        # Verify Energy Consumption Graph
        self.verify_energy_consumption()
        
        self.helper.logout()
        self.helper.tearDown()


    def verify_element(self, category, element_name):
        """General function to verify if an element is visible."""
        try:
            element_locator = self.elements[category].get(element_name)
            if not element_locator:
                raise ValueError(f"❌ '{element_name}' not found in '{category}' dictionary.")

            element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(element_locator))
            assert element.is_displayed(), f"❌ '{element_name}' is not visible!"
            print(f"✅ '{element_name}' is visible")
        except Exception as e:
            print(f"❌ Error verifying '{element_name}': {e}")

    def verify_power_meters(self):
        """Verify if all Power Meter elements (titles, gauges & labels) are visible separately."""
        print("\nChecking Power Meters...")
        
        for meter_name, elements in self.elements["power_meters"].items():
            print(f"\nChecking '{meter_name}' Meter Components...")
            
            # Verify Title
            title_locator = elements.get("title")
            if title_locator:
                try:
                    title_element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(title_locator))
                    assert title_element.is_displayed(), f"❌ '{meter_name}' Title is not visible!"
                    print(f"✅ '{meter_name}' Title is visible")
                except Exception as e:
                    print(f"❌ Error verifying '{meter_name}' Title: {e}")
            
            # Verify Gauge
            gauge_locator = elements.get("gauge")
            if gauge_locator:
                try:
                    gauge_element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(gauge_locator))
                    assert gauge_element.is_displayed(), f"❌ '{meter_name}' Gauge is not visible!"
                    print(f"✅ Gauge is visible")
                except Exception as e:
                    print(f"❌ Error verifying '{meter_name}' Gauge: {e}")
            
            # Verify Labels
            labels = {k: v for k, v in elements.items() if k not in ["title", "gauge"]}
            for label_name, label_locator in labels.items():
                try:
                    label_element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(label_locator))
                    assert label_element.is_displayed(), f"❌ '{meter_name}' {label_name} is not visible!"
                    print(f"✅ {label_name} is visible")
                except Exception as e:
                    print(f"❌ Error verifying '{meter_name}' {label_name}: {e}")

    def verify_buildings(self, category):
        """Verify if all buildings and line graphs are visible."""
        print(f"\nChecking {category.replace('_', ' ').title()}...")
        for name, locator in self.elements[category].items():
            try:
                element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(locator))
                assert element.is_displayed(), f"❌ '{name}' is not visible!"
                print(f"✅ '{name}' is visible")
            except Exception as e:
                print(f"❌ Error verifying '{name}': {e}")

    def verify_line_graphs(self):
        """Verify if all line graphs and their components are visible."""
        print("\nChecking Line Graphs...")
        
        for building, data in self.elements["line_graphs"].items():
            for section, elements in data.items():
                print(f"\nChecking '{building} - {section}' Line Graph Components...")
                
                # Verify Title
                title_locator = elements.get("title")
                if title_locator:
                    try:
                        title_element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(title_locator))
                        assert title_element.is_displayed(), f"❌ '{building} - {section}' Title is not visible!"
                        print(f"✅ '{building} - {section}' Title is visible")
                    except Exception as e:
                        print(f"❌ Error verifying '{building} - {section}' Title: {e}")
                
                # Verify Graph
                graph_locator = elements.get("graph")
                if graph_locator:
                    try:
                        graph_element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(graph_locator))
                        assert graph_element.is_displayed(), f"❌ '{building} - {section}' Graph is not visible!"
                        print(f"✅ Graph is visible")
                    except Exception as e:
                        print(f"❌ Error verifying '{building} - {section}' Graph: {e}")
                
                # Verify Labels
                labels = elements.get("labels", {})
                for label_name, label_locator in labels.items():
                    try:
                        label_element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(label_locator))
                        assert label_element.is_displayed(), f"❌ '{building} - {section}' {label_name} is not visible!"
                        print(f"✅ {label_name} label is visible")
                        label_element.click()
                        print(f"✅ {label_name} label is clicked")
                    except Exception as e:
                        print(f"❌ Error verifying '{building} - {section}' {label_name}: {e}")

    def verify_energy_consumption(self):
        """Verify if the Energy Consumption graph is visible."""
        print("\nChecking Energy Consumption...")
        try:
            title_locator = self.elements["energy_consumption"].get("title")
            if title_locator:
                title_element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(title_locator))
                assert title_element.is_displayed(), "❌ Energy Consumption Title is not visible!"
                print("✅ Energy Consumption Title is visible")

            graph_locator = self.elements["energy_consumption"].get("graph")
            if graph_locator:
                graph_element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(graph_locator))
                assert graph_element.is_displayed(), "❌ Energy Consumption Graph is not visible!"
                print("✅ Energy Consumption Graph is visible")

        except Exception as e:
            print(f"❌ Error verifying Energy Consumption: {e}")

        labels = self.elements["energy_consumption"].get("labels", {})
        for label_name, label_locator in labels.items():
            try:
                label_element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(label_locator))
                assert label_element.is_displayed(), f"❌ '{label_name}' is not visible!"
                print(f"✅ '{label_name}' is visible")
                label_element.click()
                print(f"✅ '{label_name}' label is clicked")
            except Exception as e:
                print(f"❌ Error verifying '{label_name}': {e}")  
                



if __name__ == "__main__":
    unittest.main()


# Date Filters and download button function are still not included in the script.