import psycopg2
def get_all_company_blogs_urls(company_url=''):
    try:
        connection = psycopg2.connect(
            host="helius.cskhyfjg9ihd.us-east-1.rds.amazonaws.com",
            database="helius",
            user="helius_read",
            password="22EwmwtW6R3m")

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
print(get_all_company_blogs_urls())
#print(get_all_company_blogs_urls('http://pos.toasttab.com/blog/on-the-line'))