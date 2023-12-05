from selenium.webdriver.common.by import By
from .main_nav import find_by_aria_label_attribute

"""
This is navigation for the easy apply page.
"""


def get_job_page(driver, job_id):
    job_url = f"https://www.linkedin.com/jobs/view/{job_id}/"
    driver.get(job_url)
    
def find_by_button_aria_label_attribute(driver, aria_label):
    try:
        button = driver.find_element(By.CSS_SELECTOR, f'button[aria-label="{aria_label}"]')
        return button
    except:
        return False
def uncheck_follow_company(driver):
    # Find the checkbox by its id
    try:
        checkbox = driver.find_element(By.ID, "follow-company-checkbox")
        # Check if the checkbox is selected and click to uncheck it
        if checkbox.is_selected():
            driver.execute_script("arguments[0].click();", checkbox)
    except:
        return False

def click_expand_job_description(driver):
    expand_button = driver.find_element(By.CLASS_NAME, "jobs-description__footer-button")
        # Check if the checkbox is selected and click to uncheck it
    driver.execute_script("arguments[0].click();", expand_button)


def submit_button_present(driver):
    if find_by_button_aria_label_attribute(driver, "Submit application"):
        return True
    return False

def click_submit(driver):
    button = find_by_button_aria_label_attribute(driver, "Submit application")
    if button:
        button.click()
        return True
    return False
def click_review(driver):
    button = find_by_button_aria_label_attribute(driver, "Review your application")
    if button:
        button.click()
        return True
    return False
def click_next(driver):
    button = find_by_button_aria_label_attribute(driver, "Continue to next step")
    if button:
        button.click()
        return True
    return False


def click_easy_apply_button_if_exists(driver):
    buttons = driver.find_elements(By.TAG_NAME, "button")
    for button in buttons:
        if "easy apply" in button.text.lower():
            button.click()
            return True
    return False


def question_form_present(driver):
    try:
        forms = driver.find_elements(By.TAG_NAME, "form")
        if len(forms) == 0:
             return False
        for form in forms:
            if "Additional Questions" in form.text:
                return True
        return False
    except:
        return False

def application_sent(driver):
    try:
        driver.find_element(By.ID, "post-apply-modal")
    except:
        return False
    return True

    # divs = driver.find_elements(By.TAG_NAME, "div")
    # for div in divs:
    #     if "Application sent".lower() in div.text.lower():
    #         return True
    # return False 
