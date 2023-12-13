# check_download_link
This program is used to check whether journal files on the cnki website can be downloaded successfully. It notes that the way we checked was to randomly select the year of the journal and a random volumn in it, and each journal was only randomly inspects once.

## Step for usage
1. Download the chromedriver supporting your chrome browser
2. Pass the chromedriver.exe in this repository
3. Command line of executing the program
   `python main.py --journal_list_filename journal_list.xlsx --journal_list_sheetname check_list`
