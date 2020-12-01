from datetime import datetime
from dateutil.relativedelta import relativedelta
import tweepy
from tweepy import OAuthHandler
import csv
import requests
import pytesseract
from PIL import Image
import textrazor
import urllib


relevant_date = (datetime.today() + relativedelta(months=-6))


number_of_image = 1

textrazor.api_key = "802487dc0385c08292d01d6ead89d12edc6278fd9915bbf8f7426c2e"


def get_all_tweets(company_name):
    """
     Gets the webinar details from tweets of provided company

     :param company_name: the company handle in twitter
     :return: the twitter object of the tweets
     """
    consumer_key = 'CzPmtFS34RHV78Yl3U2fRgr6V'
    consumer_secret = 'DT0SbM5JrJhbZrkpbRLhcUegKN5VYGnzWDXpIIfydhJNwJiCuC'
    access_token = '1291269809238401027-nfUpPvj1L56g5UHey0KsyV4ai727Jm'
    access_secret = 'fmNaUuFb8hNWCbFNNOO5tGb1Hyz1plZlBh2DI2uOTht4l'

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True)

    # twitter limits to 200 tweets per request, we want the entire 200
    tweet_count = 200

    # getting the tweets from twitter, we use the "extended" mode
    # because this is the way to get the full text of the tweet
    results = api.user_timeline(id=company_name, count=tweet_count, tweet_mode="extended")

    if len(results) == 0:
        print("The Company doesn't have tweets")
        return []

    while results[-1].created_at > relevant_date:
        second_tweets = search_until(results[-1].id_str, company_name)
        results = results + second_tweets

    return results


def retweet_check(tweet):
    try:
        tweet.retweeted_status.full_text = tweet.retweeted_status.full_text.lower()
    except AttributeError:  # Not a retweet
        tweet.full_text = tweet.full_text.lower()


def creating_file(company_name, tweets, file_type="w"):
    """
    Create a csv file with all the relevant details of the company webinars
    and only do that for tweets that created after six month ago.

    :param file_type: the type of file you want to be created (webinars or events)
    :param tweets: the company tweets
    :param company_name: the company twitter handle

    :return: None
    """
    with open(f"./Webinars/{company_name} webinars.csv", "w", encoding="utf-8", newline='') as ofile:
        writer = csv.DictWriter(ofile, fieldnames=["company_name", "name", "description", "link", "start_date",
                                                   "host_company_domains", "image", "tweet_link", "tweet_text",
                                                   "webinar_link", "image_link", ])
        writer.writeheader()

        if file_type == "w":
            ready_tweets = get_tweets_include_webinars(tweets)
        else:
            ready_tweets = get_tweets_include_events(tweets)

        for tweet in ready_tweets:
            # ready_tweet = check_webinar_links(tweet)
            # host_company = extract_text_from_image(tweet, 1)
            writer.writerow({
                    "company_name": company_name,
                    "tweet_link": 'https://twitter.com/%s/status/%s' % (company_name, tweet.id_str),
                    "tweet_text": tweet.full_text,
                    "image": tweet.entities['media'][0]['media_url'] if 'media' in tweet.entities else "",
                    "link": tweet.entities['urls'][0]['expanded_url'] if len(tweet.entities['urls']) != 0 else "",
                })


def get_tweets_include_events(tweets):
    # we only look for these keywords in the tweets
    key_words = ["summit", " event ", "conference", "podcast"]

    filtered_list = list(filter(lambda tweet: tweet.created_at > relevant_date, tweets))
    for tweet in filtered_list:
        retweet_check(tweet)
    relevant_tweets = list(filter(lambda tweet: any(word in tweet.full_text for word in key_words), filtered_list))
    results = remove_duplicate_webinars(relevant_tweets)
    return results


def get_tweets_include_webinars(tweets):
    # we only look for these keywords in the tweets
    key_words = ["webinar", "webcast"]

    filtered_list = list(filter(lambda tweet: tweet.created_at > relevant_date, tweets))
    for tweet in filtered_list:
        retweet_check(tweet)
    relevant_tweets = list(filter(lambda tweet: any(word in tweet.full_text for word in key_words), filtered_list))
    results = remove_duplicate_webinars(relevant_tweets)
    return results


def getting_tweets_data(tweets, company_name):
    """
     Gets the relevant data from the tweets

     :param company_name: the company twitter handle
            tweets: the  relevant tweets (tweets that were filtered by date)
     :return: the relevant data of the tweets.
     """
    global number_of_image
    key_words = ["webinar", "webcast"]
    data = []
    for tweet in tweets:
        lower_full_text = tweet.full_text.lower()
        if any(word in lower_full_text for word in key_words):
            # extract_text_from_image(tweet, number_of_image)
            relevant_data = {"company_name": company_name,
                    "tweet_link": 'https://twitter.com/%s/status/%s' % (company_name, tweet.id_str),
                    "tweet_text": tweet.full_text.encode("utf-8"),
                    "image": tweet.entities['media'][0]['media_url'] if 'media' in tweet.entities else "",
                    "link": tweet.entities['urls'][0]['expanded_url'] if len(tweet.entities['urls']) != 0 else ""}
            data.append(relevant_data)
    return data


def search_until(last_id, company_name):
    """
         Creating a request to twitter and get 200 tweets that are until a  specific date(last_date)

         :param last_id: is the max_id of the last tweet we have.
                company_name: the company twitter handle
         :return: the relevant data of the tweets.
    """
    consumer_key = 'CzPmtFS34RHV78Yl3U2fRgr6V'
    consumer_secret = 'DT0SbM5JrJhbZrkpbRLhcUegKN5VYGnzWDXpIIfydhJNwJiCuC'
    access_token = '1291269809238401027-nfUpPvj1L56g5UHey0KsyV4ai727Jm'
    access_secret = 'fmNaUuFb8hNWCbFNNOO5tGb1Hyz1plZlBh2DI2uOTht4l'

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    # max_id – Returns only statuses with an ID less than (that is, older than) or equal to the specified ID.
    result = api.user_timeline(id=company_name, count=200, tweet_mode='extended', max_id=last_id)
    return result


def remove_duplicate_webinars(tweets):
    """
             remove duplicate webinars according to webinar link.

             :param tweets: the tweets of the company
             :return: the tweets after removing the tweets that has the same webinar link.
    """
    seen = {}
    for tweet in tweets:
        if len(tweet.entities['urls']) != 0:
            expanded_url = tweet.entities['urls'][0]['expanded_url']
            try:
                tweet.entities['urls'][0]['expanded_url'] = unshorten_url(tweet.entities['urls'][0]['expanded_url'])
            except requests.exceptions.ConnectionError:
                tweet.entities['urls'][0]['expanded_url'] = expanded_url
                requests.status_code = "Connection refused"

            expanded_url = tweet.entities['urls'][0]['expanded_url']

            if expanded_url in seen.keys():
                tweets.remove(tweet)
            else:
                seen[expanded_url] = 1
    return tweets


def check_webinar_links(tweet):
    """
                 check if the webinar link is valid

                 :param tweet: the tweet of the company
                 :return: the tweet as it was if is webinar link is valid otherwise instead of webinar link it will
                 have empty string instead
    """
    if len(tweet.entities['urls']) != 0:
        try:
            response = requests.get(tweet.entities['urls'][0]['expanded_url'])
            if response.status_code != 200:
                tweet.entities['urls'][0]['expanded_url'] = ""
        except:
            pass
    return tweet


def extract_text_from_image(tweet, image_num):
    global number_of_image
    if 'media' in tweet.entities:
        image_url = tweet.entities['media'][0]['media_url']
        filename = image_num
        try:
            urllib.request.urlretrieve(image_url, f"./Webinars_Images/{filename}.jpg")
        except:
            print("couldn't save image")
        pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Shani\AppData\Local\Tesseract-OCR\tesseract.exe'

        with open(f"./Webinars_Images/{image_num}.txt", "w") as text_file:
            text_file.write(pytesseract.image_to_string(Image.open(f"./Webinars_Images/{filename}.jpg")))
        number_of_image += 1

        client = textrazor.TextRazor(extractors=["entities", "topics"])
        response = client.analyze(pytesseract.image_to_string(Image.open(f"./Webinars_Images/{filename}.jpg")))

        for entity in response.entities():
            print(entity.id, entity.freebase_types)
            # if "/business/business_operation" in entity.freebase_types:
            #     return entity.id


def unshorten_url(url):
    return requests.head(url, allow_redirects=True).url
