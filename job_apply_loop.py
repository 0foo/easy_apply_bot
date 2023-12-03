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
import pdb
from classes.FormManager import FormItemFactory, FormItem, SelectItem, InputItem, FieldSetItem
from nav.main_nav import wait_for, login
from nav import apply_nav
from time import sleep
from state.JobIds import JobIds
from state.AppliedIds import AppliedIds


job_ids = JobIds()
applied_ids = AppliedIds()

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
login(driver)

keyword="linux"

for job_id in job_ids.get_by_keyword(keyword):
    
    print(job_id)
    if not job_id:
        continue

    job_ids.delete(job_id)

    driver.refresh()
    apply_nav.get_job_page(driver, job_id)

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




