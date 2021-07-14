import os
import psycopg2
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from twitter.webinars import get_twitter_handle_by_html

def create_keyfile_dict():
    variables_keys = {
        "type": os.environ.get("SHEET_TYPE"),
        "project_id": os.environ.get("SHEET_PROJECT_ID"),
        "private_key_id": os.environ.get("SHEET_PRIVATE_KEY_ID"),
        "private_key": os.environ.get("SHEET_PRIVATE_KEY"),
        "client_email": os.environ.get("SHEET_CLIENT_EMAIL"),
        "client_id": os.environ.get("SHEET_CLIENT_ID"),
        "auth_uri": os.environ.get("SHEET_AUTH_URI"),
        "token_uri": os.environ.get("SHEET_TOKEN_URI"),
        "auth_provider_x509_cert_url": os.environ.get("SHEET_AUTH_PROVIDER_X509_CERT_URL"),
        "client_x509_cert_url": os.environ.get("SHEET_CLIENT_X509_CERT_URL")
    }
    # variables_keys = {
    #     "type": "service_account",
    #     "project_id": "newdashboard-308009",
    #     "private_key_id": "80112b60661e835d370c6c472f0efa50bc11792e",
    #     "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDChH4Ogz15WbgH\nOUF18awkBJXwLsFtpgjBbS7hou3fKdIe+eI3xGhDIgfzdifyqtR2N9KA2yG8KtdB\nQ011VN2JB0ISlNH/qc1Fbo2/iTMWixOszdFji14AaAo4y65Hxguj8Z1z+dkcwNyj\nAV1w3kGNdDF+Fz7TvXPxPUeJmXFUW0qcrASEIclPiitve4GarBOyCyD4ZiuDtoO7\ntEOtMgyjlYXrtxlLi4kcGmuv/lOmpP4c1iMjGJpFG6J189QSrD9MFiXTVWnOvWtE\nUxTNmQUKCrdNaj8ADfrin6KxiG87HDpC5HYV1I12IqTOnOYomZ9vK8FMqr7sEXC6\nQlW5tnENAgMBAAECggEABe4gIbUilKaFk8LNGhlqFBcHszDZuMwNDEiV208qTVlr\nDIK1wNl+DD3nXCbIBP/sRkZhZohHuQLdWSICJIeX0WulOgfLdy3oEivSqno2UoOe\n7+++aHiBPyXs2dprz8hb5n2hPT3qvpOqplWOUbiU6wkV0TBIPBBUjpA9tBY3fEjW\nlX4gtWw4y4zHCVYK3cBjApFvLHEbV2qBXWeGMB7oSJKjukAwosqIIYgjaN/6qKm2\nawAXBEaWzJ1+n4DFFE1Q1FikYJb2JosjKClwip8rvP0AyX5DnhuwKiATy26iIRO4\nU1k9XVl3dgqKq+f9vWh0XqovIUZzH9TEGgMbnNeDwQKBgQDteOhaW6rLPWcZIf2Z\njgF+tBuOzAfZX3aC3LXRFk6K8CWGB8GovvI75GJyAWuEKS3uBjqv6VKGHaUoN66g\nddMZyhrmqQZupXLeuOU05OJOVlkmC7OUowEFd7GqpBPDAVNhgBlwEXYOmtapIvh7\n725+xyZxjRy3UND+JF3VcPNW5QKBgQDRsaObWlDISUlvTyW6dlbx4/88V+VlSzh4\nz4EwxuyuGZDDCy0wnZ5PANhmNGrk7vBjyvJRm/hsaIOk6QPIGp6TOo27jEh61x/K\n55riuFFyQtiMEWcVbk8Jr5NDtgR9HJc1pR9/JpnX1zJEIjQ4VJAe+bIN9a3BGZmi\nJkQh/QWnCQKBgBWoVkCPZac9hV6UbAWKHvbIRE8kqn6Xpz5OFMLp7uXa+wEbSf0y\n1PLDZHsTSBP4kXjI1qdedylGIN7nHSUDOep7NTLeLXj/29cWM8k8KquMUnsWzBz9\nNMWj4e83IZpCT7FvtmIzJXo1guhQCSt8ba5gSVBH11ucokLbXDdwIrFFAoGBAI90\niqwGToum75ExwWrd+L9FLmD29N2mZzznIMfg3xyAKvP0WncO7bW4q1LIe3ShLl3n\nAn3oSTzJB36zVr330BKDFWGAKDm5oGtspR6D4Fxd9M1mPnJ/45yJvCKvjESXYa72\nhySyoL7z3tST3cvHtk0qn7BDKhqXy+4NZcEm204ZAoGAPMO1cDHEz5soj6NxAe1p\nOaojiK9lOkA1h/LvlH6rRD4meXmx8t4QJN2Ic5Epk25UtJOhIcsXvVJdtUf+sG9U\nI+VRlmNBsQ8emGx7l9HTIksD0lBj9u+KvIzldjX3koVnQGvaNnLDuqo090FE/Ofo\ntuMC+7IgFw9JUAjgc17nkyU=\n-----END PRIVATE KEY-----\n",
    #     "client_email": "dashboard@newdashboard-308009.iam.gserviceaccount.com",
    #     "client_id": "108154524811434067945",
    #     "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    #     "token_uri": "https://oauth2.googleapis.com/token",
    #     "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    #     "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/dashboard%40newdashboard-308009.iam.gserviceaccount.com"
    # }
    return variables_keys

def get_data_from_spreadsheet(spreadsheet_name,sheet_num=0):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    #creds = ServiceAccountCredentials.from_json_keyfile_name('common/service_account.json', scope)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(create_keyfile_dict(), scope)
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
    url_column, twitter_column, folder_id_column = 0, 0, 0
    headers = val_data[0]
    for col_num, header in enumerate(headers):
        if header.lower.strip() == "company url":
            url_column = col_num
        if header.lower().strip() == 'twitter':
            twitter_column = col_num
        if header.lower().strip() == 'folder id':
            folder_id_column = col_num
    val_data = val_data[1:]
    for idx, row in enumerate(val_data):
        twitter_handles[row[twitter_column]] = row[folder_id_column]
    return twitter_handles

def get_twitter_handle_from_db_by_compnay_url(company_url):
    try:
        connection = psycopg2.connect(
            host=os.environ['HOST'],
            database=os.environ['DATABASE'],
            user=os.environ['DATABASE_USER'],
            password=os.environ['DATABASE_PASSWORD'])
        cursor = connection.cursor()
        cursor.execute('select  cc.url, twitter_url  from crawler_companyprofile as ccp join crawler_company as cc on ccp.company_id = cc.id')
        # cursor.execute('select url from crawler_companyblogitem as cbi where cbi.company_blog_id = (select cb.uuid as company_id  from crawler_companyblog cb where url = %s)',(company_url,))
        records = cursor.fetchall()
        companies_profile = {}
        twitter_handle = ''
        for row in records:
            # print(idx ,":",row[0])
            companies_profile[row[0]] = row[1]
        if company_url in companies_profile.keys():
            twitter_handle = companies_profile[company_url]
            if twitter_handle is None:
                twitter_handle = ''
            else:
                twitter_handle.replace('/', '')
        if twitter_handle == '':
            twitter_handle = get_twitter_handle_by_html(company_url)
        return twitter_handle

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
