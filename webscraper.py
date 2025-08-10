author = "Vatsal Vasrhney"
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import NoSuchElementException
from csv_writer import write_participants_to_csv

def scrape_hackathon_page(hackathon_link, devpost_username, devpost_password):
    print("Starting the scraping process...")

    # Set up Chrome options to run in headless mode
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Initialize Chrome browser using Selenium Manager to handle the driver
    driver = webdriver.Chrome(options=chrome_options)

    print("Logging into Devpost...")

    # Function to log into Devpost with retry mechanism
    def login(devpost_username, devpost_password):
        login_attempts = 0
        while login_attempts < 3:
            driver.get("https://secure.devpost.com/users/login")

            # Clear username and password fields and enter new values
            driver.find_element(By.XPATH, '//*[@id="user_email"]').clear()
            driver.find_element(By.XPATH, '//*[@id="user_email"]').send_keys(devpost_username)
            driver.find_element(By.XPATH, '//*[@id="user_password"]').clear()
            driver.find_element(By.XPATH, '//*[@id="user_password"]').send_keys(devpost_password)
            time.sleep(1)
            driver.find_element(By.XPATH, '//*[@id="submit-form"]').click()

            time.sleep(3)  # Wait for a few seconds to allow the page to redirect

            if driver.current_url != "https://secure.devpost.com/users/login":
                print("Successfully logged into Devpost.")
                return True

            print("Login attempt failed. Retrying...")
            login_attempts += 1
        
        return False

    if not login(devpost_username, devpost_password):
        print("Failed to log in after 3 attempts. Exiting.")
        driver.quit()
        return []

    # Navigate to the hackathon link
    driver.get(hackathon_link)

    print(f"Scraping participants from: {hackathon_link}")

    # Click on the participants tab
    try:
        element = driver.find_element(By.XPATH, '//*[@id="challenge-navigation"]/div/div/nav/section/ul/li[3]/a')
        element.click()

        print("Clicked on the participants tab.")

        # Filter for people looking for a team
        element = driver.find_element(By.XPATH, '//*[@id="facets"]/ul[1]/li[1]/a')
        element.click()

        print("Filtered for people looking for a team.")

        # Let the list reload
        time.sleep(5)

        print("Waiting for the list to reload...")

        # Get the participants
        # Scroll down to load more participants
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            time.sleep(2)
            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        print("Scrolled down to load more participants.")

        # Extract participant information
        participants = driver.find_elements(By.CLASS_NAME, 'participant')

        print(f"Extracted {len(participants)} participants.")
        return participants

    except NoSuchElementException as e:
        print(f"Element not found: {e}")
        driver.quit()
        return []
