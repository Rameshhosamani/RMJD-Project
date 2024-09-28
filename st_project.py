from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import os

# Replace these with your actual Facebook credentials
facebook_USERNAME = os.getenv('FACEBOOK_USERNAME', 'your_email@example.com')
facebook_PASSWORD = os.getenv('FACEBOOK_PASSWORD', 'your_password')
WRONG_USERNAME = 'wrong_facebook_username'
WRONG_PASSWORD = 'wrong_facebook_password'
SEARCH_NAME = 'Sam'

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-extensions")

# Use webdriver_manager to manage ChromeDriver installation
service = Service(ChromeDriverManager().install())

# Initialize the ChromeDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

def login_facebook(username, password):
    try:
        # Open Facebook login page
        driver.get("https://www.facebook.com/")

        # Wait for the username field to be present
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )
        # Enter username and password
        username_input = driver.find_element(By.NAME, "email")
        password_input = driver.find_element(By.NAME, "pass")
        username_input.send_keys(username)
        password_input.send_keys(password)
        password_input.send_keys(Keys.RETURN)

        # Wait for the login process to complete
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@aria-label, 'Account')]"))
        )

        print("Login successful.")
        return True

    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def search_facebook(name):
    try:
        # Open Facebook homepage
        driver.get("https://www.facebook.com/")

        # Wait for the search bar to be present
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='search']"))
        )

        # Enter the name into the search bar
        search_input = driver.find_element(By.XPATH, "//input[@type='search']")
        search_input.send_keys(name)
        search_input.send_keys(Keys.RETURN)

        # Wait for search results to load and display
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[@role='main']"))
        )
        print(f"Search for '{name}' completed.")

    except Exception as e:
        print(f"An error occurred during search: {e}")

def main():
    print("\nTesting with incorrect details:")
    if not login_facebook(WRONG_USERNAME, WRONG_PASSWORD):
        print('Wrong username and password')
        return
    
    print("Testing with correct details:")
    if login_facebook(facebook_USERNAME, facebook_PASSWORD):
        search_facebook(SEARCH_NAME)

if __name__ == "__main__":
    main()
    # Keep the browser open indefinitely
    driver.quit()
