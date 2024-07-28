import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestHomePage(unittest.TestCase):
    
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:8501/")  # Adjust URL as needed
        self.driver.maximize_window()

    def tearDown(self):
        self.driver.quit()

    def test_detect_header_text(self):
        # Wait until the header element is visible
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="stHeader"]'))
        )
        
        # Test case to detect the presence of the header "AGRICULTURE TRADING PLATFORM"
        header_text = "AGRICULTURE TRADING PLATFORM"
        self.assertIn(header_text, self.driver.page_source)

    def test_find_sidebar(self):
        # Wait until the sidebar element is visible
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="stSidebar"]'))
        )
        
        # Test case to find the sidebar element
        sidebar_element = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="stSidebar"]')
        self.assertTrue(sidebar_element.is_displayed())

if __name__ == "__main__":
    unittest.main()
