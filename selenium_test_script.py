from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize the Chrome driver
driver = webdriver.Chrome()

# Open the Streamlit app
driver.get("http://localhost:8501")

# Wait for the page to load completely
time.sleep(5)  # Adjust the sleep time if necessary

try:
    # Find the input box and enter text
    input_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text']"))
    )
    input_box.send_keys("Test input")
    input_box.send_keys(Keys.RETURN)

    # Wait for the result to appear
    result = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='stMarkdown']"))
    )

    # Print the text of the result for debugging
    print("Result text:", result.text)

    # Check if the expected output is in the result text
    assert "Login Page" in result.text

except AssertionError:
    print("AssertionError: 'Expected Output' not found in the result text.")
finally:
    # Close the browser
    driver.quit()
