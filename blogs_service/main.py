import requests
import csv
from bs4 import BeautifulSoup
from xml.etree import ElementTree as etree
#import save_to_google_drive
from common.google_drive import save_to_google_drive, read_data_from_spreadsheet
from datetime import date
#from blogs_service import db_connect
from urllib.parse import urlparse

DATE = date.today()
FILE_NAME = str(DATE) + '_exported_blogs.csv'
FOLDER_ID = '135Zey3_aLf3UdDDln4cf9E6arpA0MOFm'

#
# def get_all_company_blogs_urls(company_url):
#     try:
#         connection = psycopg2.connect(
#             host="helius.cskhyfjg9ihd.us-east-1.rds.amazonaws.com",
#             database="helius",
#             user="helius_read",
#             password="22EwmwtW6R3m")
#
#         cursor = connection.cursor()
#         #cursor.execute('select url from crawler_companyblogitem as cbi where cbi.company_blog_id = (select cb.uuid as company_id  from crawler_companyblog cb where url = %s)',(company_url,))
#         cursor.execute('select url from crawler_companyblogitem')
#         records = cursor.fetchall()
#         all_blogs_urls = []
#         for row in records:
#             # print(idx ,":",row[0])
#             all_blogs_urls.append(row[0])
#
#         return all_blogs_urls
#
#     except (Exception, psycopg2.Error) as error:
#         print("Error while fetching data from PostgreSQL", error)
#
#     finally:
#         # closing database connection.
#         if connection:
#             cursor.close()
#             connection.close()
#             print("PostgreSQL connection is closed")


blogs_rss_url, companies_urls, companies_blogs_url = read_data_from_spreadsheet.export_all_values_from_spreadsheet('rss list to update from')
# blogs_rss_url = [
#     'https://salt.security/blog/rss.xml',
#     'https://info.innovid.com/blog/rss.xml'
# ]
# companies_urls = [
#     'https://salt.security',
#     'https://info.innovid.com'
# ]
# companies_blogs_url =[
#     'https://salt.security/blog',
#     'https://info.innovid.com/blog'
# ]


def get_blog_posts(rss):
    # rss = requests.get(rss).text.strip()
    # root = etree.fromstring(rss)
    URL = rss
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0"
    headers = {"user-agent": USER_AGENT}  # adding the user agent
    rss = requests.get(URL, headers=headers).text.strip()
    root = etree.fromstring(rss)
    return [[item.findtext('title'), item.findtext('link'),
             BeautifulSoup(item.findtext('description'), 'lxml').text.strip(), item.findtext('pubDate')] for item in
            root.findall('channel/item')]

def creat_csv_file():
    with open(f"./CSV_FILES/{FILE_NAME}", "w", encoding="utf-8", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Url', 'Description', 'Publish At', 'Company Url','Company blog url'])
        counter = 0
        for rss in blogs_rss_url:
            print("rss",rss)
            #all_blogs_urls = db_connect.get_all_company_blogs_urls(companies_blogs_url[counter])
            all_blogs_urls =[]
            #print("all_blogs",all_blogs_urls)
            for post in get_blog_posts(rss):
                print("post", post)
                print('url',post[1])
                url_parser = urlparse(post[1])
                #if post[1] in all_blogs_urls:
                url_parser = url_parser.netloc + url_parser.path
                print("url_parser", url_parser)
                if any(url_parser in blog_url for blog_url in all_blogs_urls):
                    print("here")
                    continue
                post.append(companies_urls[counter])
                post.append(companies_blogs_url[counter])
                writer.writerow(post)
            counter += 1
def main():
    creat_csv_file()
    save_to_google_drive.save_file_to_google_drive(FILE_NAME, FOLDER_ID)
#main()