from scraper import CheckDownloadLinks
import argparse
import utils
import test

def parse_command_line_args():
    parser = argparse.ArgumentParser(description="""parse excel files parameters""")
    parser.add_argument('--journal_list_filename', 
                        type=str, required=True,
                        help="""enter the file name of the journal check list, e.g. journal_list.xlsx""")
    parser.add_argument('--journal_list_sheetname',
                        type=str, required=True,
                        help="""enter the worksheet name in the file of journal check list, e.g. check list""")
    return vars(parser.parse_args())
    
def test_click_blank_space(checker):
    checker.navigate_to_journal_page('https://tra.oversea.cnki.net/knavi/JournalDetail?pcode=CJFD&pykm=AHMM', 1)
    # Randomly select an issue
    select_issue = checker.select_random_issue()
    # Randomly select a volumn from the selected issue
    checker.select_random_volumn(select_issue)
    # Randomly select a link from the selected volumn
    select_link = checker.select_random_link()
    # Click the download button of the link
    download_btn = checker.click_download(select_link)
    message = checker.check_file_downloading(download_btn)
    checker.click_blank_space()

if __name__ == "__main__":
    file_args = parse_command_line_args()
    checker = CheckDownloadLinks(**file_args)
    checker.check_download_links()
    checker.save_checked_list()
    checker.driver_quit()
    # test_click_blank_space(checker)
    

