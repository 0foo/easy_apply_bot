import sys
sys.path.append('./state')
sys.path.append('./classes')
sys.path.append('./nav')

from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from nav.main_nav import find_by_aria_label_attribute
from time import sleep
from nav.main_nav import login, wait_for, scroll_scrollbar, get_job_ids
from classes.Metrics import Metrics
from classes.JobLinkGenerator import JobLinkGenerator
from state.JobIds import JobIds



driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
login(driver)


# wait in case security question
wait_for(driver, By.XPATH, '//*[@aria-label="Primary Navigation"]')
print("Found Primary Nav bar, continuing")


# metric manager
metrics = Metrics()
# job link manager
job_link_generator = JobLinkGenerator()
job_link_generator.keywords="nepa"
# job id manager
job_id_state = JobIds()

print(f"Start total jobs gathered: { job_id_state.total() }")

to_break = False
while not to_break:
    # pdb.set_trace()
    # go to the job page
    jobs_page=job_link_generator.get_link()
    print(jobs_page)
    driver.get(jobs_page)
    scroll_scrollbar(driver)
    # get all the job ids from the page
    html_text = driver.page_source
    page_job_ids=get_job_ids(html_text)

    # iterate job ids and look for duplicates
    page_duplicate_count = 0
    for job_id in page_job_ids:
        if job_id_state.exists(job_id, job_link_generator.keywords):
            page_duplicate_count += 1
    duplicates_on_page = len(page_job_ids) - len(set(page_job_ids))

    # add job ides to the total_job set
    for job_id in page_job_ids:
        job_id_state.add(job_id, job_link_generator.keywords)

    # check if every job id on the page is a duplicate (means we've hit the end of the search)
    if page_duplicate_count == len(page_job_ids):
        metrics.duplicate_break_count += 1

    # cycle log update
    print("------Page Info------")
    print(f"number of page id's encountered on this page {len(page_job_ids)}")
    print(f"duplicates on page: {duplicates_on_page}")
    print(f"entire process duplicate count: {page_duplicate_count}")
    print(f"full page duplicate break count/duplicate break number {metrics.duplicate_break_count}/{metrics.duplicate_break_number}")
    print(f"total_ids: {job_id_state.total()}")
    print(f"Keywords: {job_link_generator.keywords}")


    # increment page_number, actually a job number but whatever
    job_link_generator.page_number += 12


    # check for loop break conditions
    # check if the no more results message appears or if we've hit a certain page count where every job id is a duplicate
    no_result_element = driver.find_elements(By.CLASS_NAME, "jobs-search-no-results-banner__image")
    no_match_text = "No matching jobs found." in driver.page_source
    if  no_match_text or len(no_result_element) > 0:
        print("Encountered no_match_text")
        to_break = True
    
    if metrics.duplicate_break_count > metrics.duplicate_break_number:
        to_break = True
        print("Duplicate Break Count condition.")

    # break early for testing    
    # if job_link_generator.page_number > 20:
    #     to_break = True

driver.quit()
print(f"End total jobs gathered: {job_id_state.total()}")








