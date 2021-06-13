import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_data_from_spreadsheet(spreadsheet_name ):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('common/service_account.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open(spreadsheet_name)
    # get the first sheet of the Spreadsheet
    sheet_instance = sheet.get_worksheet(0)
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


