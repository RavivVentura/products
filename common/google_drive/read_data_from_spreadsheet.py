import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_data_from_spreadsheet(spreadsheet_name,sheet_num=0):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('common/service_account.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open(spreadsheet_name)
    # get the first sheet of the Spreadsheet
    sheet_instance = sheet.get_worksheet(int(sheet_num))
    # get all the values of the data
    val_data = sheet_instance.get_all_values()
    return val_data

def get_data_from_spreadsheet_url(spreadsheet_url,sheet_num=0):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('common/service_account.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_url(spreadsheet_url)
    # get the first sheet of the Spreadsheet
    sheet_instance = sheet.get_worksheet(int(sheet_num))
    # get all the values of the data
    val_data = sheet_instance.get_all_values()
    return val_data

def export_all_values_from_spreadsheet(spreadsheet_name):
    val_data = get_data_from_spreadsheet(spreadsheet_name)
    blogs_rss_url = []
    companies_urls = []
    companies_blogs_urls = []
    for row in val_data[1:]:
        blogs_rss_url.append(row[3])
        companies_urls.append(row[0])
        companies_blogs_urls.append(row[2])
    return blogs_rss_url, companies_urls, companies_blogs_urls

def get_all_twitter_handles_and_folder_id_from_spredsheet(spreadsheet_name,sheet_num):
    val_data = get_data_from_spreadsheet(spreadsheet_name,sheet_num)
    twitter_handles = {}
    twitter_column = 0
    folder_id_column = 0
    headers = val_data[0]
    for col_num , header in enumerate(headers):
        if header.lower().strip() == 'twitter':
            twitter_column = col_num
        if header.lower().strip() == 'folder id':
            folder_id_column = col_num
    val_data = val_data[1:]
    for idx, row in enumerate(val_data):
        twitter_handles[row[twitter_column]] = row[folder_id_column]
    return twitter_handles
