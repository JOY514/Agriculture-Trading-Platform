import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

class TestSignUpPage(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.get("http://localhost:8501/") 

    def enter_user_input(self, fullname, email, password, confirm_password, location, phone):
        driver = self.driver
        try:
            # Explicit wait for elements to be visible
            fullname_input = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.NAME, "fullname"))
            )
            email_input = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.NAME, "email"))
            )
            password_input = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.NAME, "password"))
            )
            confirm_password_input = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.NAME, "confirm_password"))
            )
            location_input = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.NAME, "location"))
            )
            phone_input = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.NAME, "phone"))
            )
            
            # Enter user input
            fullname_input.send_keys(fullname)
            email_input.send_keys(email)
            password_input.send_keys(password)
            confirm_password_input.send_keys(confirm_password)
            location_input.send_keys(location)
            phone_input.send_keys(phone)
            
            # Submit the form
            submit_button = driver.find_element(By.NAME, "submit")
            submit_button.click()
            
        except TimeoutException as e:
            print(f"An element was not found: {e}")
            driver.save_screenshot('error_screenshot.png')

    def test_signup_valid_input(self):
        self.enter_user_input("John Doe", "john@example.com", "password123", "password123", "CA", "1234567890")
        # Add assertions to verify successful signup

    def test_signup_invalid_email(self):
        self.enter_user_input("John Doe", "invalid-email", "password123", "password123", "CA", "1234567890")
        # Add assertions to verify error message for invalid email

    def test_signup_password_mismatch(self):
        self.enter_user_input("John Doe", "john@example.com", "password123", "differentPassword", "CA", "1234567890")
        # Add assertions to verify error message for password mismatch

    def test_signup_non_functional(self):
        self.enter_user_input("John Doe", "", "", "", "", "")
        # Add assertions to verify error messages for empty fields

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
