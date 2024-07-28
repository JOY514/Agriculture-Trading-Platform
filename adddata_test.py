import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class TestAdminAddData(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:8501/MANAGE_DATA")
        time.sleep(5)  # Adjust sleep time as needed for page to fully load

    def test_select_start_date(self):
        # Test Case 1: Verify admin can select 'Start Date'
        start_date_input = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[1]/div/div/div/section[1]/div[1]/div[3]/div/div/div/div/div[2]/div")
        self.assertTrue(start_date_input.is_displayed(), "Start Date input field is not displayed")

    def test_select_end_date(self):
        # Test Case 2: Verify admin can select 'End Date'
        end_date_input = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[1]/div/div/div/section[1]/div[1]/div[3]/div/div/div/div/div[3]")
        self.assertTrue(end_date_input.is_displayed(), "End Date input field is not displayed")

    def test_filtered_mysql_dropdown(self):
        # Test Case 3: Verify dropdown 'Filtered MySQL Database'
        dropdown_element = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[1]/div/div/div/section[2]/div[1]/div/div/div/div[3]")
        self.assertTrue(dropdown_element.is_displayed(), "Filtered MySQL Database dropdown is not displayed")

    def test_add_new_record_button(self):
        # Test Case 4: Verify 'Add New Record to Database' button
        add_new_button = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[1]/div/div/div/section[2]/div[1]/div/div/div/div[4]/div[1]")
        self.assertTrue(add_new_button.is_displayed(), "'Add New Record to Database' button is not displayed")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
