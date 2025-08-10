author = "Vatsal Vasrhney"
import csv
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

def write_participants_to_csv(participants, filename='participants.csv'):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter='|')
        writer.writerow(['Name', 'Interests', 'Skills'])
        for participant in participants:
            try:
                name_element = participant.find_element(By.CLASS_NAME, 'user-name').find_element(By.TAG_NAME, 'a')
                name = name_element.text
            except NoSuchElementException:
                name = "Name not found"
            try:
                interests_element = participant.find_element(By.CLASS_NAME, 'fa-heart').find_element(By.XPATH, './ancestor::div[@class="large-6 columns"]')
                interests = ', '.join([interest.text for interest in interests_element.find_elements(By.CLASS_NAME, 'cp-tag')])
            except NoSuchElementException:
                interests = "Interests not found"
            try:
                skills_element = participant.find_element(By.CLASS_NAME, 'fa-tools').find_element(By.XPATH, './ancestor::div[@class="large-6 columns"]')
                skills = ', '.join([skill.text for skill in skills_element.find_elements(By.CLASS_NAME, 'cp-tag')])
            except NoSuchElementException:
                skills = "Skills not found"
            writer.writerow([name, interests, skills])

    print("Data written to participants.csv.")
