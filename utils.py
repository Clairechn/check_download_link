from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import os

chrome_options = Options()
chrome_options.add_argument("--headless")
download_directory = os.path.join(os.getcwd(), 'download')
prefs = {'download.default_directory': download_directory} # Download directory
chrome_options.add_experimental_option('prefs', prefs)
chrome_driver_path = os.path.join(os.getcwd(), 'chromedriver.exe')
service = Service(executable_path=chrome_driver_path)

def wait_for_present_element(driver, delay, xpath):
    '''Use WebDriverWait to wait for an element to be present on page'''
    obj = WebDriverWait(driver, delay).until(
        EC.presence_of_element_located((By.XPATH, xpath)))
    return obj

def wait_for_clickable_element(driver, delay, xpath):
    '''Use WebDriverWait to wait for an element to be clickable on page'''
    obj = WebDriverWait(driver, delay).until(
        EC.element_to_be_clickable((By.XPATH, xpath)))
    return obj

def switch_window(driver, window_num):
    handles_list = driver.window_handles
    driver.switch_to.window(handles_list[window_num])