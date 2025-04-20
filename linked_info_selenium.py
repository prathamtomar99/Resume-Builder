import time
import os
import tempfile
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import getpass
from dotenv import load_dotenv
import os
from typing import List

load_dotenv()  # This loads the .env file
def extract_about_from_linkedin(linkedin_url, debug_mode=True):
    # Temporary directory for user data (used when debugging)
    temp_dir = os.path.join(tempfile.gettempdir(), f'chrome_profile_{time.time()}')

    # Configure Chrome options
    chrome_options = Options()

    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")  #directory

    # Disable features that aren't necessary
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36")

    # Initialize the driver (either a new session or an existing one via remote debugging)
    driver = webdriver.Chrome(options=chrome_options)

    # Create a debug directory if it doesn't exist
    if not os.path.exists("debug"):
        os.makedirs("debug")

    # Navigate to the target LinkedIn profile
    # print(f"Navigating to profile: {linkedin_url}")
    driver.get(linkedin_url)
    time.sleep(7)  # Allow the profile page to load

    # Save initial page source for debugging purposes
    with open("debug/initial_page.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)

    # Scroll down to reveal content
    # print("Scrolling to reveal content...")
    for i in range(7):
        driver.execute_script(f"window.scrollTo(0, {i * 500});")
        time.sleep(1)

    # Try to locate the About section header
    # print("Looking for About section header...")
    elements = driver.find_elements(By.CLASS_NAME, "ph5")
    
    test = ""
    count= 0
    for elem in elements:
        if count>=5:
            break;
        # print(elem.text)  # Print element text
        # print(elem)  # Print the element object
        test += elem.get_attribute('innerHTML')
        count += 1
    

    return test

# # Example usage
# if __name__ == "__main__":
#     linkedin_url = "https://www.linkedin.com/in/hritesh-maikap-7aaa76246/"
    
#     extract_about_from_linkedin(linkedin_url)