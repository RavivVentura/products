import requests
import csv
from bs4 import BeautifulSoup
from xml.etree import ElementTree as etree
from common.google_drive import save_to_google_drive, read_data_from_spreadsheet
from datetime import date
from blogs_service import db_connect
from urllib.parse import urlparse

DATE = date.today()
FILE_NAME = str(DATE) + '_exported_blogs.csv'
FOLDER_ID = '135Zey3_aLf3UdDDln4cf9E6arpA0MOFm'
#blogs_rss_url, companies_urls, companies_blogs_url = [],[],[]
blogs_rss_url, companies_urls, companies_blogs_url = read_data_from_spreadsheet.export_all_blogs_data_from_spreadsheet('rss list to update from')

def get_blog_posts(rss):
    URL = rss
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0"
    headers = {"user-agent": USER_AGENT}  # adding the user agent
    parser = etree.XMLParser(encoding='UTF-8',)
    rss = requests.get(URL, headers=headers).text.strip()
    # if '<?xml version="1.0" encoding="UTF-8"?>' not in rss:
    #     rss = '<?xml version="1.0" encoding="UTF-8"?>' + rss
    root = etree.fromstring(rss, parser=parser)
    return [[item.findtext('title'), item.findtext('link'),
             BeautifulSoup(item.findtext('description'), 'lxml').text.strip(), item.findtext('pubDate')] for item in
            root.findall('channel/item')]

def creat_csv_file():
    with open(f"./CSV_FILES/{FILE_NAME}", "w", encoding="utf-8", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Url', 'Description', 'Published At', 'Company Url','Company blog url'])
        counter = 0
        all_blogs_urls = db_connect.get_all_company_blogs_urls()
        for rss in blogs_rss_url:
            print("rss",rss)
            #all_blogs_urls =[]
            #print("all_blogs",all_blogs_urls)
            try:
                for post in get_blog_posts(rss):
                    print('url',post[1])
                    url_parser = urlparse(post[1])
                    url_parser = url_parser.netloc + url_parser.path
                    if url_parser[-1] == '/':
                        url_parser = url_parser[:-1]
                    print("url_parser", url_parser)
                    if any(url_parser in blog_url for blog_url in all_blogs_urls):
                        print("here")
                        continue
                    post.append(companies_urls[counter])
                    post.append(companies_blogs_url[counter])
                    writer.writerow(post)
            except Exception as e:
                print("Failed to get blog post for rss url:{}, exception:{}".format(rss, e))
            counter += 1
            print("Success to get blog post for rss url:{}".format(rss))
def main():
    creat_csv_file()
    save_to_google_drive.save_file_to_google_drive(FILE_NAME, FOLDER_ID)
#main()