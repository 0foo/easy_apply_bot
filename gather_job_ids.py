""""
Searches a linkedin site for jobids matching a keyword(s).
Input your keyword(s) into keyword variable and run this: python3 gather_job_ids.py.
"""

import sys
import pdb
import requests
from bs4 import BeautifulSoup
import re

sys.path.append("./state")
sys.path.append("./classes")
sys.path.append("./nav")

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver

from nav.main_nav import login, wait_for, scroll_scrollbar, get_job_ids, check_text
from state.JobIds import JobIds
from state.AppliedIds import AppliedIds
from state.DeletedIds import DeletedIds
from classes.JobLinkGenerator import JobLinkGenerator
from classes.Metrics import Metrics
from classes.Requests import Requests


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
login(driver)

wait_for(driver, By.XPATH, '//*[@aria-label="Primary Navigation"]')
print("Found Primary Nav bar, continuing")

metrics = Metrics()
job_link_generator = JobLinkGenerator()
job_id_state = JobIds()
applied_ids = AppliedIds()
deleted_ids = DeletedIds()

print(f"Start total jobs gathered: { job_id_state.total() }")

TO_BREAK = False
while not TO_BREAK:
    jobs_page = job_link_generator.get_link()
    print(jobs_page)
    driver.get(jobs_page)
    
    # pdb.set_trace()
    scroll_scrollbar(driver)
    html_text = driver.page_source
    page_job_ids = get_job_ids(html_text)

    # iterate job ids and look for duplicates
    PAGE_DUPLICATE_COUNT = 0
    for job_id in page_job_ids:
        if job_id_state.exists(job_id, job_link_generator.keywords):
            PAGE_DUPLICATE_COUNT += 1
    DUPLICATES_ON_PAGE = len(page_job_ids) - len(set(page_job_ids))

    # add job ides to the total_job set
    for job_id in page_job_ids:
        DO_ADD=True
        if deleted_ids.item_exists(job_id) or job_id_state.item_exists(job_id) or deleted_ids.item_exists(job_id):
            DO_ADD=False

        if DO_ADD:
            job_page_url = f"https://www.linkedin.com/jobs/view/{job_id}/"
            if not check_text(job_page_url,ignored, required, job_id):
                continue
            job_id_state.add(job_id, job_link_generator.keywords)
            print(f"{job_id} added successfully")


    # check if every job id on the page is a duplicate (means we've hit the
    # end of the search)
    if PAGE_DUPLICATE_COUNT == len(page_job_ids):
        metrics.duplicate_break_count += 1

    # cycle log update
    print("------Page Info------")
    print(f"number of page id's encountered on this page {len(page_job_ids)}")
    print(f"duplicates on page: {DUPLICATES_ON_PAGE}")
    print(f"entire process duplicate count: {PAGE_DUPLICATE_COUNT}")
    print((
            "full page duplicate break count/duplicate break number" +
            f"{metrics.duplicate_break_count}/{metrics.duplicate_break_number}"
    ))
    print(f"total_ids: {job_id_state.total()}")
    print(f"Keywords: {job_link_generator.keywords}")

    # increment page_number, actually a job number but whatever
    job_link_generator.page_number += 12

    # check for loop break conditions
    # check if the no more results message appears or if we've hit a certain
    # page count where every job id is a duplicate
    no_result_element = driver.find_elements(
        By.CLASS_NAME, "jobs-search-no-results-banner__image"
    )
    no_match_text = "No matching jobs found." in driver.page_source
    if no_match_text or len(no_result_element) > 0:
        print("Encountered no_match_text")
        TO_BREAK = True

    if metrics.duplicate_break_count > metrics.duplicate_break_number:
        TO_BREAK = True
        print("Duplicate Break Count condition.")

    # break early for testing
    # if job_link_generator.page_number > 20:
    #     TO_BREAK = True

driver.quit()
print(f"End total jobs gathered: {job_id_state.total()}")
