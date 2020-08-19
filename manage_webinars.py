import sys
import tweepy
from webinars import get_tweets
from webinars import creating_file
from webinars import getting_tweets_data
from datetime import datetime
import csv


def filter_date_tweet(start_date, tweets):
    """
         Gets the tweets that created after a specific date(start_date)
         :param start_date: the date that from him we want the tweets
                tweets: the tweets of the company profile (200 because of the twitter limit)
         :return: the tweets that created after start_date
    """
    filtered_tweets = []
    for tweet in tweets:
        if tweet.created_at > start_date:
            filtered_tweets.append(tweet)
    return filtered_tweets


def monthly_update(start_date, file):
    """
             Create a csv file with all the companies webinars since the start date
             :param start_date: the date that from him we want the tweets
                    file: file with all the companies names that we want to update their webinars
             :return: none
    """
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
            tweets_data = getting_tweets_data(relevant_tweets, company)
            for tweet in tweets_data:
                writer.writerow({
                        "company_name": tweet["company_name"],
                        "tweet_link": tweet["tweet_link"],
                        "tweet_text": tweet["tweet_text"],
                        "image_link": tweet["image_link"],
                        "webinar_link": tweet["webinar_link"]
                    })


if __name__ == "__main__":
    # checking if the command is to create a file for new company or making a monthly update
    if "csv" in sys.argv[1]:
        file_name = sys.argv[1]
        date = sys.argv[2]
        start_date = datetime.strptime(date, "%d/%m/%Y")
        monthly_update(start_date, file_name)
    else:
        company_name = sys.argv[1]
        results = get_tweets(company_name)
        creating_file(company_name, results)



