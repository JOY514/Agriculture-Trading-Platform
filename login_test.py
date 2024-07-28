from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest

class TestLoginPage(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:8501/")

    def tearDown(self):
        self.driver.quit()

    def test_login_empty_input(self):
        # Locate the email and password input elements
        email_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="textInputRootElement"] input'))
        )
        password_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="stTextInput"] input[type="password"]'))
        )
        
        # Clear any existing input (though it should be empty if we didn't enter anything)
        email_input.clear()
        password_input.clear()
        
        # Click the Login button
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="stButton"] button'))).click()
        
        # Check for error message for empty fields
        try:
            error_message = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="stNotificationContentError"] p'))
            )
            self.assertEqual(error_message.text, "Invalid email or password format")
        except Exception as e:
            self.fail(f"Test failed: {e}")


    def test_login_invalid_email(self):
        # Test case logic for invalid email
        email_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="textInputRootElement"] input'))
        )
        email_input.clear()
        email_input.send_keys("JAJA@gmail.com")
        
        password_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="stTextInput"] input[type="password"]'))
        )
        password_input.clear()
        password_input.send_keys("Plm123456")
        
        # Click the Login button
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="stButton"] button'))).click()
        
        # Check for error message for empty fields
        try:
            error_message = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="stNotificationContentError"] p'))
            )
            self.assertEqual(error_message.text, "Invalid email or password")
        except Exception as e:
            self.fail(f"Test failed: {e}")

    def test_login_invalid_password(self):
        # Test case logic for invalid password
        email_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="textInputRootElement"] input'))
        )
        email_input.clear()
        email_input.send_keys("abc@gmail.com")
        
        password_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="stTextInput"] input[type="password"]'))
        )
        password_input.clear()
        password_input.send_keys("abc123")
        
        # Click the Login button
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="stButton"] button'))).click()
        
        # Check for error message for empty fields
        try:
            error_message = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="stNotificationContentError"] p'))
            )
            self.assertEqual(error_message.text, "Invalid email or password format")
        except Exception as e:
            self.fail(f"Test failed: {e}")

    def test_login_valid_input(self):
        # Test case logic for valid login input
        email_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="textInputRootElement"] input'))
        )
        email_input.clear()
        email_input.send_keys("abc@gmail.com")
            
        password_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="stTextInput"] input[type="password"]'))
        )
        password_input.clear()
        password_input.send_keys("Plm123456")
            
        # Click the Login button
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="stButton"] button'))).click()
            
        # Check for success message
        try:
            print("Waiting for success message element...")
            success_message = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="stNotificationContentSuccess"] p'))
            )
            print("Success message element found.")
            self.assertEqual(success_message.text, "Login successful!")
            print("Login successful!")
        except Exception as e:
            self.fail(f"Test failed: {e}")
            

if __name__ == "__main__":
    unittest.main()



# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import unittest

# class TestLoginPage(unittest.TestCase):

#     def setUp(self):
#         self.driver = webdriver.Chrome()
#         self.driver.get("http://localhost:8501/")

#     def tearDown(self):
#         self.driver.quit()

#     def test_login_empty_fields(self):
#         # Locate the email and password input elements
#         email_input = WebDriverWait(self.driver, 10).until(
#             EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="textInputRootElement"] input'))
#         )
#         password_input = WebDriverWait(self.driver, 10).until(
#             EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="stTextInput"] input[type="password"]'))
#         )
        
#         # Clear any existing input (though it should be empty if we didn't enter anything)
#         email_input.clear()
#         password_input.clear()
        
#         # Click the Login button
#         WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="stButton"] button'))).click()
        
#         # Check for error message instead of alert
#         error_message = WebDriverWait(self.driver, 10).until(
#             EC.visibility_of_element_located((By.ID, "error_message"))
#         )
#         self.assertEqual(error_message.text, "Invalid email or password format")

#     def test_login_invalid_email(self):
#         # Test case logic for invalid email (similar to your implementation)
#         email_input = WebDriverWait(self.driver, 10).until(
#             EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="textInputRootElement"] input'))
#         )
#         email_input.clear()
#         email_input.send_keys("Ibrahim@gmail.com")
        
#         password_input = WebDriverWait(self.driver, 10).until(
#             EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="stTextInput"] input[type="password"]'))
#         )
#         password_input.clear()
#         password_input.send_keys("Plm123456")
        
#         # Click the Login button
#         WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="stButton"] button'))).click()
        
#         # Check for error message
#         error_message = WebDriverWait(self.driver, 10).until(
#             EC.visibility_of_element_located((By.ID, "error_message"))
#         )
#         self.assertEqual(error_message.text, "Invalid email address")

#     def test_login_invalid_password(self):
#         # Test case logic for invalid password (similar to your implementation)
#         email_input = WebDriverWait(self.driver, 10).until(
#             EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="textInputRootElement"] input'))
#         )
#         email_input.clear()
#         email_input.send_keys("abc@gmail.com")
        
#         password_input = WebDriverWait(self.driver, 10).until(
#             EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="stTextInput"] input[type="password"]'))
#         )
#         password_input.clear()
#         password_input.send_keys("abc123")
        
#         # Click the Login button
#         WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="stButton"] button'))).click()
        
#         # Check for error message
#         error_message = WebDriverWait(self.driver, 10).until(
#             EC.visibility_of_element_located((By.ID, "error_message"))
#         )
#         self.assertEqual(error_message.text, "Invalid password")

#     def test_login_valid_input(self):
#         # Test case logic for valid login input
#         email_input = WebDriverWait(self.driver, 10).until(
#             EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="textInputRootElement"] input'))
#         )
#         email_input.clear()
#         email_input.send_keys("abc@gmail.com")
            
#         password_input = WebDriverWait(self.driver, 10).until(
#             EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="stTextInput"] input[type="password"]'))
#         )
#         password_input.clear()
#         password_input.send_keys("Plm123456")
            
#         # Click the Login button
#         WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="stButton"] button'))).click()
            
#         # Check for success message
#         try:
#             print("Waiting for success message element...")
#             success_message = WebDriverWait(self.driver, 200).until(
#                 EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="stNotificationContentSuccess"] p'))
#             )
#             print("Success message element found.")
#             self.assertEqual(success_message.text, "Login successful!")
#             print("Login successful!")
#         except Exception as e:
#             self.fail(f"Test failed: {e}")


# if __name__ == "__main__":
#         unittest.main()


