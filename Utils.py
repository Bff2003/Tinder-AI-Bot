from selenium import webdriver
import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Utils:
    @staticmethod
    def wait_for_element(driver, xpath, by=By.XPATH, tries=5, timeout=1, raise_exception=False):
        for i in range(tries):
            element = Utils.try_to_find_element(driver, xpath, by=by)
            if element is not None:
                return element
            time.sleep(timeout)
        
        if raise_exception:
            raise Exception("Element not found")
        else:
            return None

    @staticmethod
    def wait_for_elements(driver, xpath, by=By.XPATH, tries=5, timeout=1, raise_exception=False):
        for i in range(tries):
            elements = Utils.try_to_find_elements(driver, xpath, by=by)
            if elements is not None and len(elements) > 0:
                return elements
            time.sleep(timeout)
        
        if raise_exception:
            raise Exception("Element not found")
        else:
            return None

    @staticmethod
    def random_sleep(min, max):
        sleep_time = random.randint(min, max)
        time.sleep(sleep_time)
    
    @staticmethod
    def try_to_find_element(driver, xpath, by=By.XPATH):
        try:
            element = driver.find_element(by=by, value=xpath)
            return element
        except:
            return None
    
    @staticmethod
    def try_to_find_elements(driver, xpath, by=By.XPATH):
        try:
            elements = driver.find_elements(by=by, value=xpath)
            return elements
        except:
            return None
    
    @staticmethod
    def click_button(driver, button):
        button2 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(button))
        button2.click()

