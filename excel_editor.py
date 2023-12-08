import openpyxl


def read_excel(filepath, ws_name=None):
    wb = openpyxl.load_workbook(filepath, data_only=True)
    if ws_name is None:
        ws = wb.worksheets[0]
    else:
        ws = wb[ws_name]
    return ws


def get_journal_urls(ws):
    journal_url_list = [
        ws.cell(row=i, column=17).value for i in range(2, ws.max_row)]
    return journal_url_list


def get_journal_names(ws):
    journal_name_list = [
        ws.cell(row=i, column=4).value for i in range(2, ws.max_row)]
    return journal_name_list


def save_to_excel(filepath, data_list):
    new_wb = openpyxl.Workbook()
    new_ws = new_wb.active

    for row in data_list:
        new_ws.append(row)

    new_wb.save(filepath)
