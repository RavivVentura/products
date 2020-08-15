
import tweepy
from tweepy import OAuthHandler
import csv
import sys


def get_tweets(company_name):
    """
     Gets the webinar details from tweets of provided company

     :param company_name: the company handle in twitter
     :return: None
     """
    consumer_key = 'CzPmtFS34RHV78Yl3U2fRgr6V'
    consumer_secret = 'DT0SbM5JrJhbZrkpbRLhcUegKN5VYGnzWDXpIIfydhJNwJiCuC'
    access_token = '1291269809238401027-nfUpPvj1L56g5UHey0KsyV4ai727Jm'
    access_secret = 'fmNaUuFb8hNWCbFNNOO5tGb1Hyz1plZlBh2DI2uOTht4l'

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True)

    name = company_name

    # twitter limits to 200 tweets per request, we want the entire 200
    tweet_count = 200

    # getting the tweets from twitter, we use the "extended" mode
    # because this is the way to get the full text of the tweet
    results = api.user_timeline(id=name, count=tweet_count, tweet_mode="extended")

    with open(f"{name} webinars.csv", "w",  newline='') as ofile:
        writer = csv.DictWriter(ofile, fieldnames=["company_name", "name", "description", "link", "start_date",
                                                   "host_company_domains", "image", "tweet_link", "tweet_text",
                                                   "webinar_link", "image_link", ])
        writer.writeheader()

        # we only look for these keywords in the tweets
        key_words = ["webinar", "webcast"]

        for tweet in results:
            lower_full_text = tweet.full_text.lower()
            if any(word in lower_full_text for word in key_words):
                writer.writerow({
                    "company_name": company_name,
                    "tweet_link": 'https://twitter.com/%s/status/%s' % (name, tweet.id_str),
                    "tweet_text": tweet.full_text,
                    "image_link": tweet.entities['media'][0]['media_url'] if 'media' in tweet.entities else "",
                    "webinar_link": tweet.entities['urls'][0]['expanded_url'] if len(tweet.entities['urls']) != 0 else ""
                })


if __name__ == "__main__":
    get_tweets(sys.argv[1])
