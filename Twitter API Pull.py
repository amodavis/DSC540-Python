# --------------------------------------------------------------------------------------
# File: Exercise_9.2.py
# Name: Amie Davis
# Date: 10/24/2019
# Course: DSC540 - Data Preparation
# Assignment Number: 9.2
#
# Purpose:  Ch 13 Review: Pulling Data from APIs
#
# Websites Utilized: http://twitter.com
#
# Usage: Uses Python 3.7.
#        Developed using PyCharm 2019.1.3.
#
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
# Function oauth_req()
#
# Description:  Sends request, authenticating with oauth and returns response
#
# Parameters:   url: website URL
#               key: Access token key
#               secret: Access token secret
#               api_key: Consumer API key
#               api_secret: Consumer API secret
#
# Returns:      website response with content
#
import oauth2

def oauth_req(url, key, secret, api_key, api_secret):

    http_method = "GET"
    http_headers = None

    consumer = oauth2.Consumer(key=api_key, secret=api_secret)
    token = oauth2.Token(key=key, secret=secret)
    client = oauth2.Client(consumer, token)

    # Note that body=post_body will fail since null is passed.
    # Removed that argument since it is not required.
    resp, content = client.request(url, method=http_method, headers=http_headers)

    return content

# --------------------------------------------------------------------------------------
# Function store_tweet()
#
# Description:  Stores json object into database table
#
# Parameters:   item: json object with data to store
#
# Returns:      No return value
#
def store_tweet(table_name, item):

    import dataset

    # Open sqlite database connection
    db = dataset.connect('sqlite:///data_wrangling.db')

    # Create new table to store data
    # Create explicitly to avoid primary key assignment
    table = db.create_table(table_name, primary_id=False)

    item_json = item._json.copy()
    for key, value in item_json.items():
        # Remove any dictionary items
        if isinstance(value, dict):
            item_json[key] = str(value)

    # Insert record into table
    table.insert(item_json)

    # Output can be found by querying the db.

    # --------------------------------------------------------------------------------------
# Main function
#
def main():

    ####################################################
    # Part I - Create a Twitter API Key and Access Token
    ####################################################
    # Twitter Consumer API keys
    # Wt2e6JLi5f9wQ5M8E8PU88tb3(API key)
    # mDPI3JsDZn0zAC1wKOEWCRMx7f2bafdfmqPHzjTmOsVXgi7Q84(API secret key)

    # Twitter Access tokens
    # 1155826467831521280-WVEn2jlWjZ350Xg5Y7jvviJt6kD65B (Access token)
    # kZn3ODX03ANCOmyHKO8AsrAVut9HWBZsKAqfRGoqQbcR9(Access token secret)

    #########################################################
    # Part II - Do a single data pull from Twitter’s REST API
    #########################################################

    # Set keys
    API_KEY = 'Wt2e6JLi5f9wQ5M8E8PU88tb3'
    API_SECRET = 'mDPI3JsDZn0zAC1wKOEWCRMx7f2bafdfmqPHzjTmOsVXgi7Q84'
    TOKEN_KEY = '1155826467831521280-WVEn2jlWjZ350Xg5Y7jvviJt6kD65B'
    TOKEN_SECRET = 'kZn3ODX03ANCOmyHKO8AsrAVut9HWBZsKAqfRGoqQbcR9'

    # Pull data from Twitter REST API
    url = 'https://api.twitter.com/1.1/search/tweets.json?q=%23popeindc'
    data = oauth_req(url, TOKEN_KEY, TOKEN_SECRET, API_KEY, API_SECRET)

    # Output json results to file
    with open("data/hashchildlabor.json", "wb") as data_file:
        data_file.write(data)

    #######################################################################
    # Part III - Execute multiple queries at a time from Twitter’s REST API
    #######################################################################
    import tweepy

    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(TOKEN_KEY, TOKEN_SECRET)

    api = tweepy.API(auth)

    query = '#childlabor'
    cursor = tweepy.Cursor(api.search, q=query, lang="en")

    # Store APT results in db table
    for page in cursor.pages():
        for item in page:
            store_tweet('tweets', item)

    #######################################################
    # Part IV - Do a data pull from Twitter’s Streaming API
    #######################################################
    from tweepy.streaming import StreamListener
    from tweepy import OAuthHandler, Stream

    class Listener(StreamListener):

        def on_data(self, data):
            print(data)
            return True

    auth = OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(TOKEN_KEY, TOKEN_SECRET)

    # Stream Twitter data and exports to terminal
    stream = Stream(auth, Listener())
    stream.filter(track=['child labor'])

#----------------------------------------------------------------
# Run program

# Global imports

main()
