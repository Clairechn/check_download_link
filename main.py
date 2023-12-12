from scraper import CheckDownloadLinks
import argparse

def parse_command_line_args():
    parser = argparse.ArgumentParser(description="""parse excel files parameters""")
    parser.add_argument('--journal_list_filename', 
                        type=str, required=True,
                        help="""enter the file name of the journal check list, e.g. journal_list.xlsx""")
    parser.add_argument('--journal_list_sheetname',
                        type=str, required=True,
                        help="""enter the worksheet name in the file of journal check list, e.g. check list""")
    return vars(parser.parse_args())
    
if __name__ == "__main__":
    file_args = parse_command_line_args()
    checker = CheckDownloadLinks(**file_args)
    checker.check_download_links()
    checker.save_checked_list()
    checker.driver_quit()


