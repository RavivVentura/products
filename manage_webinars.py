import sys
import tweepy
from webinars import get_tweets
from webinars import creating_file
from webinars import getting_tweets_data
from datetime import datetime
import csv


def filter_date_tweet(start_date, tweets):
    filtered_tweets = []
    for tweet in tweets:
        if tweet.created_at > start_date:
            filtered_tweets.append(tweet)
    return filtered_tweets


def monthly_update(start_date, file):
    month = start_date.month
    year = start_date.year
    with open(f"./Updates/{month} {year} webinars.csv", "w", newline='') as ofile:
        writer = csv.DictWriter(ofile, fieldnames=["company_name", "name", "description", "link", "start_date",
                                                   "host_company_domains", "image", "tweet_link", "tweet_text",
                                                 "webinar_link", "image_link"])
        writer.writeheader()
        companies_file = csv.DictReader(open(file))
        for row in companies_file:
            company = row['twitter']
            tweets = get_tweets(company)
            relevant_tweets = filter_date_tweet(start_date, tweets)
            tweets_data = getting_tweets_data(relevant_tweets, month, year, company)
            for tweet in tweets_data:
                writer.writerow({
                        "company_name": tweet["company_name"],
                        "tweet_link": tweet["tweet_link"],
                        "tweet_text": tweet["tweet_text"],
                        "image_link": tweet["image_link"],
                        "webinar_link": tweet["webinar_link"]
                    })


if __name__ == "__main__":
    if "csv" in sys.argv[1]:
        file_name = sys.argv[1]
        date = sys.argv[2]
        start_date = datetime.strptime(date, "%d/%m/%Y")
        monthly_update(start_date, file_name)
    else:
        company_name = sys.argv[1]
        results = get_tweets(company_name)
        creating_file(company_name, results)



