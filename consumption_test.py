import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class TestUserViewForecast(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        # Update the URL to reflect the actual running Streamlit app
        self.driver.get("http://localhost:8501/FORECAST_CONSUMPTION_AREA")
        time.sleep(5)  # Wait for the page to fully load

    def test_select_state_sidebar(self):
        # Test Case 1: Verify user can select state in the sidebar
        select_state_input = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[1]/div/div/div/section[1]/div[1]/div[3]/div/div/div/div/div[2]/div/div/div/div[1]/div[2]/input")
        self.assertTrue(select_state_input.is_displayed(), "Select State input field is not displayed")

    def test_select_date_sidebar(self):
        # Test Case 2: Verify user can select date in the sidebar
        select_date_label = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[1]/div/div/div/section[1]/div[1]/div[3]/div/div/div/div/div[3]/div/label")
        self.assertTrue(select_date_label.is_displayed(), "Select Date label is not displayed")

    def test_analytics_dropdown(self):
        # Test Case 3: Verify clicking on ANALYTICS dropdown
        analytics_dropdown_summary = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[1]/div/div/div/section[2]/div[1]/div/div/div/div[3]/details/summary")
        analytics_dropdown_summary.click()

        # Wait for the dropdown content to be visible
        analytics_dropdown_content = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[1]/div/div/div/section[2]/div[1]/div/div/div/div[3]/details/div")
        WebDriverWait(self.driver, 10).until(EC.visibility_of(analytics_dropdown_content))

        self.assertTrue(analytics_dropdown_content.is_displayed(), "Analytics dropdown did not expand")

    def test_forecasted_consumption_area_header(self):
        # Test Case 5: Verify "Forecasted Consumption Area" header
        forecasted_header = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[1]/div/div/div/section[2]/div[1]/div/div/div/div[5]/div/div/div/div/h3")
        self.assertEqual(forecasted_header.text, "Forecasted Consumption Area", "Header text does not match expected")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
