from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from excel_editor import *
import utils
import random
from selenium.webdriver.common.action_chains import ActionChains


class CheckDownloadLinks():
    '''
    Check if the download links of the journals is valid by randomly choosing one link from every journal
    '''

    def __init__(self, journal_list_file="journal_list.xlsx", ws_name="Only List_406"):
        self.journal_list_file = journal_list_file
        self.journal_ws = read_excel(self.journal_list_file, ws_name)
        self.journal_url_list = get_journal_urls(self.journal_ws)
        self.driver = webdriver.Chrome(options=utils.chrome_options)

    def check_download_links(self):
        for journal_index, journal_url in enumerate(self.journal_url_list, 1):
            self.driver.get(journal_url)

            # Wait to load page
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="leftYearTree"]')))

            # Randomly select an issue
            select_issue = self.select_random_issue()

            # Randomly select a volumn from the selected issue
            self.select_random_volumn(select_issue)

            # Randomly select a link from the selected volumn
            select_link = self.select_random_link()

            # Click the download button of the link
            self.click_download(select_link)

    def navigate_to_journal_page(self, journal_url, journal_index):
        try:
            self.driver.get(journal_url)
        except Exception as e:
            print("Journal {} not detected".format(journal_index))
            pass
        else:
            print("Journal {}".format(journal_index))

    def wait_for_present_element(self, delay, xpath):
        '''Use WebDriverWait to wait for an element to present on page'''
        obj = WebDriverWait(self.driver, delay).until(
            EC.presence_of_element_located((By.XPATH, xpath)))
        return obj

    def select_random_issue(self):
        all_issues = self.driver.find_elements(
            By.XPATH, '//*[@id="yearissue+0"]/dl[contains(@id, "_Year_Issue")]')
        select_issue = all_issues[random.randint(1, len(all_issues)-1)]
        # print("Number of selected issue: ", select_issue.text)
        select_issue.click()

        return select_issue

    def select_random_volumn(self, select_issue):
        all_volumns = select_issue.find_elements(By.XPATH, './dd/a')
        select_volumn = all_volumns[random.randint(1, len(all_volumns)-1)]
        # print("Number of selected volumn: ", select_volumn.text)
        select_volumn.click()
        self.driver.implicitly_wait(10)
        # Wait to load page
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="CataLogContent"]/dd[1]')))

    def select_random_link(self):
        all_links = self.driver.find_elements(
            By.XPATH, '//*[@id="CataLogContent"]/dd')
        select_link = all_links[random.randint(1, len(all_links)-1)]
        # print("Text of selected link: ", select_link.text)

        return select_link

    def click_download(self, select_link):
        download_btn = WebDriverWait(select_link, 10).until(
            EC.presence_of_element_located((By.XPATH, './ul/li[1]/a[1]')))
        actions = ActionChains(self.driver)
        actions.move_to_element(download_btn)
        actions.pause(3)
        actions.click().perform()
