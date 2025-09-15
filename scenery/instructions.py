import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# def get_(django_testcase, url):
#     # NOTE: if needed for the landing
#     ...

def get_pm_sujets0_a_generate_html(django_testcase, url, data, query_parameters):
    # print("Waiting...")
    wait = WebDriverWait(django_testcase.driver, 60)  # 10 second timeout
    wait.until(
        EC.presence_of_element_located((By.ID, "loading-message"))
    )
    wait.until(
        lambda driver: "text-success" in driver.find_element(By.ID, "loading-message").get_attribute("class")
    )

    time.sleep(1)



    k = 8

    fragment_wrappers = django_testcase.driver.find_elements(By.CLASS_NAME, "fragment-wrapper")

    print("HERE", len(fragment_wrappers))

    for wrapper in fragment_wrappers[:k]: 
        django_testcase.driver.execute_script("arguments[0].remove();", wrapper)
    


    # if int(query_parameters["nbStudents"]) > 1:
    fragment_wrappers = django_testcase.driver.find_elements(By.CSS_SELECTOR, '.fragment-wrapper[data-f_type="h2_"]')
    for wrapper in fragment_wrappers:
        django_testcase.driver.execute_script("arguments[0].remove();", wrapper)

    fragment_wrappers = django_testcase.driver.find_elements(By.CSS_SELECTOR, '.fragment-wrapper[data-f_type="hr_"]')
    for wrapper in fragment_wrappers:
        django_testcase.driver.execute_script("arguments[0].remove();", wrapper)

    time.sleep(1)


    # time.sleep(20)