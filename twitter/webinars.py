import pendulum
import tweepy
from tweepy import OAuthHandler
import csv
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pytesseract
from PIL import Image #need to be install poetry
import textrazor
import urllib #need to be install poetry
from twitter.google_drive_save import save_file_to_google_drive


from_date = pendulum.today().subtract(months=12)
# relevant_date = (datetime.today() + relativedelta(months=-6))


number_of_image = 1

# textrazor.api_key = "bd75d8e752e4708e9ed10de767e405bd8967b87b093b98ac92676ec5"
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
    last_date = pendulum.instance(results[-1].created_at)
    while last_date > from_date:
        second_tweets = search_until(results[-1].id_str, company_name)
        if not second_tweets:
            return results
        results = results + second_tweets
    return results

def retweet_check(tweet):
    try:
        tweet.retweeted_status.full_text = tweet.retweeted_status.full_text.lower()
    except AttributeError:  # Not a retweet
        tweet.full_text = tweet.full_text.lower()


def creating_file(company_name, tweets, folder_id, file_type="w"):
    """
    Create a csv file with all the relevant details of the company webinars
    and only do that for tweets that created after six month ago.

    :param file_type: the type of file you want to be created (webinars or events)
    :param tweets: the company tweets
    :param company_name: the company twitter handle
    :param folder_id: the id of the drive folder (in the url)

    :return: None
    """
    file_name = str(company_name) + '_webinars.csv'
    with open(f"./CSV_FILES/{file_name}", "w", encoding="utf-8", newline='') as ofile:
        writer = csv.DictWriter(ofile, fieldnames=["company_name", "name", "description", "link", "start_date",
                                                   "host_company_domains", "image", "tweet_link", "tweet_text",
                                                   "webinar_link", "image_link", ])
        writer.writeheader()

        if file_type == "w":
            ready_tweets = get_tweets_include_webinars(tweets)
            print("got webinar tweets")
            if len(ready_tweets) == 0:
                no_ready_tweets_message = "couldn't find any webinar on Twitter, please search manually on Google and on company's website."
                writer.writerow({
                    "company_name": no_ready_tweets_message,
                })
        else:
            ready_tweets = get_tweets_include_events(tweets)

        for tweet in ready_tweets:
            # ready_tweet = check_webinar_links(tweet)
            results = extract_text_from_image(tweet)
            print("extracted text from image")
            if not results:
                start_date = " "
                webinar_name = " "
                description = " "
            else:
                start_date = results[0]
                webinar_name = results[1]
                description = results[2]

            writer.writerow({
                    "company_name": company_name,
                    "tweet_link": 'https://twitter.com/%s/status/%s' % (company_name, tweet.id_str),
                    "tweet_text": tweet.full_text,
                    "image": tweet.entities['media'][0]['media_url'] if 'media' in tweet.entities else "",
                    "link": tweet.entities['urls'][0]['expanded_url'] if len(tweet.entities['urls']) != 0 else "",
                    "start_date": start_date,
                    "name": webinar_name,
                    "description": description,
                })
    save_file_to_google_drive(file_name, folder_id)


def get_tweets_include_events(tweets):
    # we only look for these keywords in the tweets
    key_words = ["summit", " event ", "conference", "podcast"]

    filtered_list = list(filter(lambda tweet: tweet.created_at > from_date, tweets))
    for tweet in filtered_list:
        retweet_check(tweet)
    relevant_tweets = list(filter(lambda tweet: any(word in tweet.full_text for word in key_words), filtered_list))
    results = remove_duplicate_webinars(relevant_tweets)
    return results


def get_tweets_include_webinars(tweets):
    # we only look for these keywords in the tweets
    key_words = ["webinar", "webcast"]

    filtered_list = list(filter(lambda tweet: pendulum.instance(tweet.created_at) > from_date, tweets))
    # for tweet in filtered_list:
    #     #     retweet_check(tweet)
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
            results = extract_text_from_image(tweet)
            if not results:
                start_date = " "
                webinar_name = " "
                description = " "
            else:
                start_date = results[0]
                webinar_name = results[1]
                description = results[2]

            relevant_data = {"company_name": company_name,
                    "name": webinar_name,
                    "tweet_link": 'https://twitter.com/%s/status/%s' % (company_name, tweet.id_str),
                    "tweet_text": tweet.full_text.encode("utf-8"),
                    "image": tweet.entities['media'][0]['media_url'] if 'media' in tweet.entities else "",
                    "link": tweet.entities['urls'][0]['expanded_url'] if len(tweet.entities['urls']) != 0 else "",
                    "start_date": start_date,
                    "description": description}
            data.append(relevant_data)
    print(f"finished getting {company_name} data")
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

    # api.user_timeline has a bug and sometimes returns the same result over and over again. so the if statment handle
    # that by checking if the result last item has the same id as last_id if so return empty list because we don't need
    # to continue getting tweets.
    if not result or last_id == result[-1].id_str:
        return []

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


def extract_text_from_image(tweet):
    """
         saving the webinar image to a local folder (if the tweet has image) and using pytessract to extract
         the text from the image to a txt file. running text razor on the text.

         :param tweet: the tweet object
         :return: array of webinar date and webinar name
    """
    global number_of_image
    if 'media' in tweet.entities:
        image_url = tweet.entities['media'][0]['media_url']
        filename = number_of_image
        try:
            # saving the webinar's image
            urllib.request.urlretrieve(image_url, f"Webinars_Images/{filename}.jpg")
        except:
            print("couldn't save image")

        pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

        with open(f"Webinars_Images/{filename}.txt", "w") as text_file:
            text_file.write(pytesseract.image_to_string(Image.open(f"Webinars_Images/{filename}.jpg")))
            # os.remove(filename)
        number_of_image += 1

        client = textrazor.TextRazor(extractors=["entities", "topics", "phrases"])
        try:
            response = client.analyze(pytesseract.image_to_string(Image.open(f"Webinars_Images/{filename}.jpg")))
        except:
            response = ""

        webinar_date = extract_webinar_date(tweet, response)
        # webinar_name = extract_webinar_name(tweet, response)
        description = ""
        try:
            html = urlopen(tweet.entities['urls'][0]['expanded_url'])
            bsh = BeautifulSoup(html.read(), 'html.parser')
            title = "" if not bsh.title else bsh.title.text
            if len(title.split(" ")) > 3:
                webinar_name = title
                # need to decide if to check if the url includes zoom.us
                if webinar_name == "Webinar Registration - Zoom" or "zoom.us" in tweet.entities['urls'][0]['expanded_url']:
                    webinar_name = bsh.find("strong").text
                    div = bsh.findAll("div", {"class": "form-group horizontal"})[1]
                    description = div.find("div").text.strip()
                    time = bsh.findAll("div", {"class": "form-group horizontal"})[2]
                    webinar_date = time.find("div").text.strip()
                if "event.on24.com" in tweet.entities['urls'][0]['expanded_url']:
                    webinar_name = bsh.findAll("span", {"name": "title"})[0]
                    time = bsh.findAll("span", {"name": "date"})[1]
                    div = bsh.findAll("div", {"class": "summary-section section"})[1]
                    description = div.find("span", {"class": "summary"})
            else:
                webinar_name = ""
        except:
            webinar_name = ""

        result = [webinar_date, webinar_name, description]

        return result


def unshorten_url(url):
    """
    Expand shorten urls.
    :param url: the event/webinar url address
    :return: the expand/original url of the event/webinar
    """
    try:
        expand_url = requests.head(url, allow_redirects=True).url
    except requests.exceptions.TooManyRedirects:
        expand_url = url

    return expand_url


def extract_webinar_date(tweet, entities):
    """
    Extracting the webinar date in three ways. The first is to extract it from the image text.
    The second is to extract it from the tweet text using text razor.
    The third is to find the words "Tomorrow/Today" and calculate the date from the tweet created date.
    :param tweet: the tweet object
    :param entities: the response from text razor.
    :return: the date of the event if we succeeded else empty string
    """
    wanted_entities = ["Date", "Time"]
    if entities:
        webinar_date = date_entity_check(entities, wanted_entities)
    else:
        webinar_date = ""

    # if we couldn't get the webinar date from the image we will try to get it from the tweet text.
    if not webinar_date:
        client = textrazor.TextRazor(extractors=["entities", "topics"])
        try:
            response = client.analyze(tweet.full_text)
            webinar_date = date_entity_check(response, wanted_entities)
        except:
            webinar_date = ""



    if not webinar_date:
        array_words = ["Today", "Tomorrow"]
        if array_words[0] in tweet.full_text:
            webinar_date = tweet.created_at
        if array_words[1] in tweet.full_text:
            webinar_date = pendulum.instance(tweet.created_at).add(days=1)
    if not webinar_date:
        return None

    final_date = webinar_date_check(webinar_date, tweet)
    if not final_date:
        return ""

    return final_date


def date_entity_check(entities, entities_type):
    """

    :param entities: entities from text razor response
    :param entities_type: the type we want
    :return:
    """
    date_entity = None
    for entity in entities.entities():
        if any(word in entity.dbpedia_types for word in entities_type):
            try:
                date_entity = pendulum.parse(entity.id)
            except:
                date_entity = None
            return date_entity

    return date_entity


def webinar_date_check(date_entity, tweet):
    """
    checking if the year of the date is correct. checking if the numbers of days between start date and tweet created
    date is less than one year. if it's true than we don't change the date, else we change the year of start date
    to be the year of tweet created date
    :param date_entity: the date from text razor
    :param tweet: the tweet object
    :return: the correct date
    """
    date = pendulum.instance(date_entity)
    created_date = pendulum.instance(tweet.created_at)
    delta = date.diff(created_date).in_days()

    if int(delta) > 364:
        date = date.set(year=created_date.year, month=date.month, day=date.day).to_datetime_string()

    return date


def extract_webinar_name(tweet, response):
    """
         extract webinar name in both ways. the first is running text razor on the image text and the second
         is running text razor on the tweet text.

         :param tweet: the tweet object.
         :param response: text razor response for the image text.
         :return: optional names of the webinar.
    """
    # trying to extract the name from image text
    # optional_names = get_sentence(response)

    # trying to extract the name from tweet text
    client = textrazor.TextRazor(extractors=["entities", "topics", "phrases"])
    response = client.analyze(tweet.full_text)
    optional_names = get_sentence(response)

    return optional_names


def get_sentence(response):
    """
         find the sentence containing the wanted entity type.

         :param response: text razor response.
         :return: optional sentences that include the webinar name.
    """
    entities_type = ["/book/book_subject", "/film/film_subject", "/time/event"]
    wanted_entities = []
    for entity in response.entities():
        if any(word in entity.freebase_types for word in entities_type):
            wanted_entities.append(entity.matched_text)

    sentences = []
    # we want to have all sentences but we can't get them as a string so we need to concat each word in the sentence
    for sentence in response.sentences():
        sent = ''
        # Forming a sentence from words
        for w in sentence.words:
            sent = sent + ' ' + w.token

        sentences.append(sent)

    wanted_sentences = []
    for sentence in sentences:
        for word in wanted_entities:
            if word in sentence:
                wanted_sentences.append(sentence)

    # for x in wanted_sentences:
    #     print("wanted sentence: ", x)
    if not wanted_sentences:
        return ""

    return wanted_sentences[0]
