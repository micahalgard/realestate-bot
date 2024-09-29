from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from django.core.management.base import BaseCommand
from realestate.models import Property
from django.utils import timezone
import json
import time
import re

class Command(BaseCommand):
    help = "scrape data and save to database"

    def attach_to_session(self, executor_url):
        driver = webdriver.Remote(
            command_executor=executor_url,
            options=webdriver.ChromeOptions()
            )
        driver.implicitly_wait(1)
        return driver

    ## execute search
    def execut_search(self, driver, street):
        driver.switch_to.frame("middle")
        search = driver.find_element(By.ID, "SearchVal1")
        submit = driver.find_element(By.NAME, "cmdGo")
        search.clear()
        search.send_keys(street)
        submit.submit()
        driver.switch_to.default_content()

    def open_in_new_tab(self, driver, element, switch_to_new_tab=True):
        # Do some actions
        ActionChains(driver) \
            .move_to_element(element) \
            .key_down(Keys.COMMAND) \
            .click() \
            .key_up(Keys.COMMAND) \
            .perform()
        
    def match_regex(self, text, regex, group):
        match = re.search(regex, text)
        if match:
            if(group):
                return match.group(group)
            else:
                return match.group()
        else:
            return 

    ## click link
    def find_link_text(self, driver):
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

    def find_house_info(self, driver):
            time.sleep(1)
            driver.switch_to.frame("bottom")
            form = driver.find_element(By.TAG_NAME, "form")
            f_table = form.find_elements(By.TAG_NAME, "td")

            parsel_id_regex = r'\d{1,10}-\d{1,10}(?:-[A-Za-z0-9]+)?'
            address_number_regex = r"Location\s+(\d+)"
            address_street_regex = r"Location\s+\d+\s+(.*)"
            parsel_id = self.match_regex(f_table[2].text, parsel_id_regex, None)
            address_number = int(self.match_regex(f_table[0].text, address_number_regex, 1))
            address_street = self.match_regex(f_table[0].text, address_street_regex, 1)
            owner = f_table[8].text
            zoning = f_table[22].text
            sale_date = f_table[28].text
            sale_price = f_table[32].text
            legal_reference = f_table[30].text
            seller = f_table[34].text
            assessment_year = f_table[43].text
            land_area = f_table[51].text
            building_value = f_table[45].text
            extra_features_value = f_table[49].text
            land_value = f_table[53].text
            total_value = f_table[57].text
            narrative_description = f_table[59].text

            self.save_property(
                address_number=address_number,
                address_street=address_street,
                parsel_id=parsel_id,
                owner=owner,
                zoning=zoning,
                sale_date=sale_date,
                sale_price=sale_price,
                legal_reference=legal_reference,
                seller=seller,
                assessment_year=assessment_year,
                land_area=land_area,
                building_value=building_value,
                extra_features_value=extra_features_value,
                land_value=land_value,
                total_value=total_value,
                narrative_description=narrative_description
            )
    
    def save_property(self, **kwargs):
        obj, created = Property.objects.update_or_create(
            parcel_id=kwargs.get('parsel_id'),
            defaults={
                'address_number': kwargs.get('address_number'),
                'address_street': kwargs.get('address_street'),
                'address_city': "Beverly",
                'owner': kwargs.get('owner'),
                'zoning': kwargs.get('zoning'),
                'sale_date': kwargs.get('sale_date'),
                'sale_price': kwargs.get('sale_price'),
                'legal_reference': kwargs.get('legal_reference'),
                'seller': kwargs.get('seller'),
                'assessment_year': kwargs.get('assessment_year'),
                'land_area': kwargs.get('land_area'),
                'building_value': kwargs.get('building_value'),
                'extra_features_value': kwargs.get('extra_features_value'),
                'land_value': kwargs.get('land_value'),
                'total_value': kwargs.get('total_value'),
                'narrative_description': kwargs.get('narrative_description'),
                'last_updated': timezone.now(),
            }
        )
        return obj, created

    def click_links(self, driver, parcel_ids):
        base_handle = driver.current_window_handle
        for p in parcel_ids:
            driver.switch_to.default_content()
            driver.switch_to.frame("bottom")
            m = driver.find_element(By.LINK_TEXT, p)
            self.open_in_new_tab(driver, m)
            tabs = driver.window_handles
            driver.switch_to.window(tabs[1])
            self.find_house_info(driver)
            driver.close()
            driver.switch_to.window(base_handle)
            
        
    def handle(self, *args, **options):
        browser = webdriver.Chrome() 
        executor_url = browser.command_executor._url
        driver = self.attach_to_session(executor_url=executor_url)
        BASE_URL = 'https://beverly.patriotproperties.com'
        driver.get(BASE_URL)
        with open('webscraper/streets_data/street_sample.json', 'r') as json_file:
            data = json.load(json_file)
        for street in data:
            self.execut_search(driver, street)
            parcel_text = self.find_link_text(driver)
            self.click_links(driver, parcel_text)