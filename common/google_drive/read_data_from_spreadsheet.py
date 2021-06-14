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
    for row in val_data:
        if row[0] == 'Company URL':
            continue
        blogs_rss_url.append(row[3])
        companies_urls.append(row[0])
        companies_blogs_urls.append(row[2])
    return blogs_rss_url, companies_urls, companies_blogs_urls

def get_all_twitter_handles_from_spredsheet(spreadsheet_name,sheet_num):
    val_data = get_data_from_spreadsheet(spreadsheet_name,sheet_num)
    twitter_handles = []
    for row in val_data:
        if row[0] == 'Company URL':
            continue
        twitter_handles.append(row[2])
    #print("twitter_handles", twitter_handles)
    return twitter_handles