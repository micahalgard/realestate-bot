from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import json
import time

def attach_to_session(executor_url):
    driver = webdriver.Remote(
        command_executor=executor_url,
        options=webdriver.ChromeOptions()
        )
    driver.implicitly_wait(1)
    return driver

## execute search
def execut_search(driver, street):
    driver.switch_to.frame("middle")
    search = driver.find_element(By.ID, "SearchVal1")
    submit = driver.find_element(By.NAME, "cmdGo")
    search.clear()
    search.send_keys(street)
    submit.submit()
    driver.switch_to.default_content()

def open_in_new_tab(driver, element, switch_to_new_tab=True):
    # Do some actions
    ActionChains(driver) \
        .move_to_element(element) \
        .key_down(Keys.COMMAND) \
        .click() \
        .key_up(Keys.COMMAND) \
        .perform()

## click link
def find_link_text(driver):
    driver.switch_to.frame("bottom")
    t_body = driver.find_element(By.ID, "T1")
    rows = t_body.find_elements(By.TAG_NAME, "tr")
    parcel_ids = []
    for r in rows:
        column = r.find_elements(By.TAG_NAME, "td")
        if len(column) > 0:
            first_column = column[0]
            parcel_id = first_column.text
            parcel_ids.append(parcel_id)
    return parcel_ids

def find_house_info(driver):
        time.sleep(1)
        driver.switch_to.frame("bottom")
        form = driver.find_element(By.TAG_NAME, "form")
        f_table = form.find_elements(By.TAG_NAME, "td")
        property_data = f_table[60].text
        return property_data

def click_links(driver, parcel_ids):
    base_handle = driver.current_window_handle
    for p in parcel_ids:
        driver.switch_to.default_content()
        driver.switch_to.frame("bottom")
        m = driver.find_element(By.LINK_TEXT, p)
        open_in_new_tab(driver, m)
        tabs = driver.window_handles
        driver.switch_to.window(tabs[1])
        property_data = find_house_info(driver)
        print(property_data)
        driver.close()
        driver.switch_to.window(base_handle)
        
if __name__ == "__main__":
    browser = webdriver.Chrome() 
    executor_url = browser.command_executor._url
    driver = attach_to_session(executor_url=executor_url)
    BASE_URL = 'https://beverly.patriotproperties.com'
    driver.get(BASE_URL)
    with open('streets_data/street_sample.json', 'r') as json_file:
        data = json.load(json_file)
    for street in data:
        execut_search(driver, street)
        parcel_text = find_link_text(driver)
        click_links(driver, parcel_text)