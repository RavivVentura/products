import psycopg2
import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


def get_all_company_blogs_urls():
    try:
        connection = psycopg2.connect(
            host=os.environ['HOST'],
            database=os.environ['DATABASE'],
            user=os.environ['DATABASE_USER'],
            password=os.environ['DATABASE_PASSWORD'])
        cursor = connection.cursor()
        cursor.execute('select url from crawler_companyblogitem')
        # cursor.execute('select url from crawler_companyblogitem as cbi where cbi.company_blog_id = (select cb.uuid as company_id  from crawler_companyblog cb where url = %s)',(company_url,))
        records = cursor.fetchall()
        all_blogs_urls = []
        for row in records:
            # print(idx ,":",row[0])
            all_blogs_urls.append(row[0])

        return all_blogs_urls

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
