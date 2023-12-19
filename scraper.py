from selenium import webdriver
import os
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchWindowException, StaleElementReferenceException
from excel_editor import *
import utils
from tqdm import tqdm
from utils import *
import random
import time
from selenium.webdriver.common.action_chains import ActionChains

class CheckDownloadLinks():
    '''
    Check if the download links of the journals is valid by randomly choosing one link from every journal
    '''
    def __init__(self, **kwargs):
        self.journal_list_file = kwargs["journal_list_filename"]
        self.journal_df = read_excel_df(self.journal_list_file, kwargs["journal_list_sheetname"])
        self.driver = webdriver.Chrome(service=utils.service, options=utils.chrome_options)

    def check_download_links(self):
        for journal_index, journal_url in (tqdm(self.journal_df['URL'].items(), total=self.journal_df.shape[0])):
            # Navigate to the journal page
            self.navigate_to_journal_page(journal_url, journal_index)
            # Randomly inspect links in the journal 
            attempts = 0
            message = "Faild to inspect"
            while attempts <= 5:
                try:
                    # Randomly select an issue
                    select_issue = self.select_random_issue()
                    # Randomly select a volumn from the selected issue
                    self.select_random_volumn(select_issue)
                    # Randomly select a link from the selected volumn
                    select_link = self.select_random_link()
                    # Click the download button of the link
                    download_btn = self.click_download(select_link)
                    message = self.check_file_downloading(download_btn)
                except:
                    attempts += 1
                    print("Retry the random inspection...", attempts)
                else:
                    break
            self.write_message_to_df(message, journal_index)
        # self.journal_df[['期刊代碼', '測試']]

    def navigate_to_journal_page(self, journal_url, journal_index):
        try:
            self.driver.get(journal_url)
        except Exception as e:
            print("Failed to navigate")
            self.write_message_to_df("Faild to navigate", journal_index)
            pass
        else:
            # Wait to load page
            wait_for_present_element(self.driver, 10, '//*[@id="leftYearTree"]')
            print("Journal {}".format(journal_index))

    def select_random_issue(self):
        all_issues = self.driver.find_elements(
            By.XPATH, '//*[@id="yearissue+0"]/dl[contains(@id, "_Year_Issue")]')
        select_issue = all_issues[random.randint(1, len(all_issues)-1)]
        print("Number of selected issue: ", select_issue.text)
        select_issue.click()

        return select_issue

    def select_random_volumn(self, select_issue):
        all_volumns = select_issue.find_elements(By.XPATH, './dd/a')
        select_volumn = all_volumns[random.randint(1, len(all_volumns)-1)]
        print("Number of selected volumn: ", select_volumn.text)
        select_volumn.click()
        # Wait to load page
        wait_for_clickable_element(self.driver, 30, '//*[@id="CataLogContent"]/dd[1]')

    def select_random_link(self):
        all_links = self.driver.find_elements(
            By.XPATH, '//*[@id="CataLogContent"]/dd')
        select_link = all_links[random.randint(1, len(all_links)-1)]
        print("Text of selected link: ", select_link.text)
        return select_link

    def click_download(self, select_link):
        download_btn = wait_for_present_element(select_link, 30, './ul/li[1]/a[1]')
        attempt = 1
        while len(self.driver.window_handles) == 1:
            if attempt <= 10:
                print("Clicking the download btn...", attempt)
                self.switch_to_window(0)
                actions = ActionChains(self.driver)
                actions.move_to_element(download_btn)
                actions.pause(3)
                actions.move_by_offset(0, 0)
                actions.pause(3)
                actions.click().perform()
                attempt += 1
            else:
                print("Faild to click download button")
                return
        time.sleep(5)
        return download_btn

    def check_file_downloading(self, download_btn):
        message = self.wait_for_file_downloading(download_btn)
        time.sleep(5)
        if message is not None:
            print("Faild to download file: ", message)
            return message
        else:
            if self.directory_is_empty(utils.download_directory):
                print("Error deteced")
            else:
                print("File downloaded successfully")
                self.remove_download_file(utils.download_directory)
                message = "ok"
                return message
        
    def wait_for_file_downloading(self, download_btn):
        attempt = 1
        while (len(self.driver.window_handles)) > 1:
            if attempt <= 10:
                print("Waiting for file downloading...", attempt)
                try:
                    self.switch_to_window(1)
                    message = self.get_download_message()
                    if message is not None:
                        self.driver.close()
                        self.switch_to_window(0)
                        return message
                    else:
                        time.sleep(5)
                        attempt += 1
                        continue
                except NoSuchWindowException as e:
                    break
            else:
                message = download_btn.get_attribute('href')
                return message
        return None

    def get_download_message(self):
        try:
            message = wait_for_present_element(self.driver, 15, '/html/body/div/p')
            return message.text
        except TimeoutException as e:
            return None

    def switch_to_window(self, window_index):
        handles_list = self.driver.window_handles
        self.driver.switch_to.window(handles_list[window_index])
    
    def directory_is_empty(self, path):
        return True if not os.listdir(path) else False

    def remove_download_file(self, path):
        for filename in os.listdir(path):
            print("Download file: ", filename)
            filepath = os.path.join(path, filename)
            os.remove(filepath)

    def write_message_to_df(self, message, jorunal_index, column="測試"):
        self.journal_df.at[jorunal_index, column] = message

    def save_checked_list(self, filepath="checked_list.xlsx", ws_name="Checked"):
        print("Save checked list to excel...")
        save_to_excel(filepath, self.journal_df, ws_name)

    def driver_quit(self):
        self.driver.quit()