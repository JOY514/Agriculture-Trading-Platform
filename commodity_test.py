import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class TestFrequencyDistributionPage(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        # Update the URL to reflect the actual running Streamlit app
        self.driver.get("http://localhost:8501/FREQUENCY_DISTRIBUTIONS")
        time.sleep(5)  # Wait for the page to fully load

    def test_page_title(self):
        # Test Case 1: Verify Page Title
        self.assertEqual(self.driver.title, "Home", "Page title is not 'Home'")

    def test_success_message(self):
        # Test Case 2: Verify Presence of Success Message
        success_message = self.driver.find_element(By.XPATH, "//*[contains(text(), 'FREQUENCY DISTRIBUTION TABLE')]")
        self.assertIsNotNone(success_message, "Success message 'FREQUENCY DISTRIBUTION TABLE' not found")

    def test_sidebar_image(self):
        # Test Case 3: Verify Sidebar Image
        sidebar_image = self.driver.find_element(By.XPATH, "//*[@id='root']/div[1]/div[1]/div/div/div/section[1]/div[1]/div[3]/div/div/div/div/div/div/div/div")
        self.assertIsNotNone(sidebar_image, "Sidebar image not found")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
