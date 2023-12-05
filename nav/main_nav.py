from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from time import sleep
import os,sys,json, requests, re, pdb, json
from classes.Requests import Requests


# Get the path to the directory above the current script's directory
current_script_directory = os.path.dirname(__file__)
parent_directory = os.path.dirname(current_script_directory)
sys.path.append(parent_directory)
my_requests = Requests()



"""
This is navigation for main parts of the site.
"""
def login(driver):
    username=""
    password=""
    with open('config.json', 'r') as file:
        data = json.load(file)
        username = data["username"]
        password = data["password"]

    # Step 1: Open the LinkedIn homepage
    driver.get("https://www.linkedin.com/home")
    sleep(3)

    # Step 2: Set window size (this step is usually optional)
    driver.set_window_size(1850, 1173)

    # Step 3: Click on the element with the id 'session_key' (usually the username field)
    # This step might not be necessary unless it's to focus the field before typing.
    # driver.find_element(By.ID, 'session_key').click()

    # Step 4: Type the email into the 'session_key' field
    driver.find_element(By.ID, 'session_key').send_keys(username)

    # Step 5: Click on the element with the id 'session_password' (usually the password field)
    # This step might not be necessary unless it's to focus the field before typing.
    # driver.find_element(By.ID, 'session_password').click()

    # Step 6: Type the password into the 'session_password' field
    driver.find_element(By.ID, 'session_password').send_keys(password)

    # Step 7: Click the sign-in button. Assuming the button can be selected by the given CSS selector.
    driver.find_element(By.CSS_SELECTOR, '[data-id="sign-in-form__submit-btn"]').click()

    # wait for success, this gives time to fill out the captcha
    try:
        wait_for(driver, By.XPATH, '//*[@aria-label="Primary Navigation"]', sleep_time=1, max_check=45)
    except:
        
        driver.refresh()
        
    try:
        wait_for(driver, By.XPATH, '//*[@aria-label="Primary Navigation"]', sleep_time=1, max_check=10)
    except:
        driver.refresh()

def scroll_scrollbar(driver):
    # there's an ajax loading scrollbar that needs to be scrolled in order to extract the full extent of job_ids on the page
    wait_for(driver, By.CLASS_NAME, 'jobs-search-results-list')
    scrollable_div = driver.find_element(By.CLASS_NAME, 'jobs-search-results-list')
    driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
    sleep(3)

def get_job_ids(html_text):
    # list of:
    # * easy apply jobs 
    # * posted within last week 
    # * in the United state
    # each job element looks like this: '<div data-job-id="3772470826"></div>'
    soup = BeautifulSoup(html_text, 'html.parser')
    soup_search = soup.find_all(attrs={'data-job-id': True})
    out = []
    for element in soup_search:
        out.append(element['data-job-id'])
    return out

def find_by_aria_label_attribute(driver, aria_label):
    try:
        elements_with_aria_label = driver.find_elements(By.XPATH, f'//*[@aria-label="{aria_label}"]')
        if len(elements_with_aria_label) > 0:
            return elements_with_aria_label
        return False
    except:
        return False

def wait_for(driver, search_type, selector_string, sleep_time=5, max_check=50):
    max_check_count = 0
    while True:
        elements = driver.find_elements(search_type, selector_string)
        if len(elements) > 0:
            print(f"Waiting for:{selector_string}: True")
            return True
        print(f"Waiting for:{selector_string}: False")
        max_check_count += 1
        if max_check_count >= max_check:
            print(f"Wait_for exceeded max check count: {max_check}. Exception thrown.")
            raise Exception("Exceed max wait time.")
        sleep(sleep_time)


def check_text(job_page_url, ignored, required, job_id):
    print(f"Checking {job_page_url} for required/ignored keywords.")
    try:
        parent_text = my_requests.get(job_page_url).text
    except:
        raise("check_text method not working!!")

    soup = BeautifulSoup(parent_text, 'html.parser')
    the_text = soup.find(class_="details").text.replace("\n", " ")
    job_text = re.sub(r"\s+" ," ", the_text)

    for req in required:
        if req.lower() not in job_text.lower():
            print(f"{req} not in job text, ignoring {job_id}")
            return False
        
    for ign in ignored:
        if ign.lower() in job_text.lower():
            print(f"{ign} present in job text, ignoring {job_id}")
            return False
        
    return True

