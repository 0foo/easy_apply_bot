import json
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
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pdb
from classes.FormManager import FormItemFactory, FormItem, SelectItem, InputItem, FieldSetItem
from classes.Config import Config
from nav.main_nav import wait_for, login, get_config
from nav import apply_nav
from time import sleep
from state.JobIds import JobIds
from state.AppliedIds import AppliedIds
from state.DeletedIds import DeletedIds


config= Config()
required=config.required
ignored=config.ignored
keywords=config.keywords


job_ids = JobIds()
applied_ids = AppliedIds()
deleted_ids = DeletedIds()

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
login(driver)


for job_id in job_ids.get_by_keyword(keywords):
    if deleted_ids.item_exists(job_id):
        continue

    print(job_id)
    print(f"https://www.linkedin.com/jobs/view/{job_id}/")
    if not job_id:
        continue

    job_ids.delete(job_id)
    deleted_ids.add(job_id)

    the_l = len(job_ids.get_by_keyword(keywords))
    print(f"Jobs left in keyword(s): {keywords} set: {the_l}")

    driver.refresh()
    apply_nav.get_job_page(driver, job_id)



    # text search
    TO_CONT=False
    try:
        wait_for(driver, By.CLASS_NAME, "job-view-layout")
        apply_nav.click_expand_job_description(driver)
        job_text = driver.find_element(By.CLASS_NAME, "job-view-layout").text
        for req in required:
            if req.lower() not in job_text.lower():
                print(f"{req} not in job text, ignoring")
                TO_CONT=True
        for ign in ignored:
            if ign.lower() in job_text.lower():
                print(f"{ign} present in job text, ignoring")
                TO_CONT=True
    except:
        pdb.set_trace()

    if TO_CONT:
        sleep(4)
        continue

    # wait for easy apply button and click
    try:
        wait_for(driver, By.XPATH,  "//button[contains(@aria-label, 'Easy Apply')]", sleep_time=1, max_check=7)
    except:
        continue
    sleep(2)
    # click easy apply button
    for i in range(0, 5):
        button = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Easy Apply')]")
        driver.execute_script("arguments[0].click();", button)
        applied_ids.add(job_id)
        try:
            if wait_for(driver, By.TAG_NAME,  "form", sleep_time=1, max_check=3):
                break
        except:
            continue
    
    if apply_nav.submit_button_present(driver):
        apply_nav.uncheck_follow_company(driver)
        # try:
        #     apply_nav.click_submit(driver)
        # except:
        #     pass
        # continue


    if apply_nav.application_sent(driver):
        print("Application sent div found, SHOULD NOT BE PRESENT!")
        pdb.set_trace()

    # form nav
    while True:
        try: 
            try:
                driver.find_element(By.TAG_NAME, 'form')
                continue
            except Exception as e:
                print(e)
                print("Form not found.")
                
                if apply_nav.submit_button_present(driver):
                    apply_nav.uncheck_follow_company(driver)
                    continue

                sleep(1)
                if apply_nav.application_sent(driver):
                    print("Application sent div found")
                    if not applied_ids.item_exists(job_id):
                        applied_ids.add(job_id)
                break
            
        except Exception as e:
            print(e)
            continue


print("Completed processing all job ids. Application process finished successfully, exiting.")




