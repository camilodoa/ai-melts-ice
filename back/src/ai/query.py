import requests

'''
Contains the classes used for querying APIs that have information on ICE
'''

class Querier():
    '''
    Superclass for objects used to query
    '''
    def __init__(self):
        pass

    def query(self):
        pass


class Syracuse(Querier):
    '''
    Object used to query Syracuse deportation database

    Website: https://trac.syr.edu/phptools/immigration/remove/
    '''
    def __init__(self):
        self.dates = 191
        self.cities = 385

    def query(self, city):
        url = (
            'https://trac.syr.edu/phptools/immigration/remove/graph.php?'
            'stat=count&timescale=fymon&depart_city='
            '[CITY]&timeunit=number'
        ).replace('[CITY]', city)

        headers = {
            'content-type': 'application/json'
        }

        response = requests.get(url, headers=headers).json()

        return response


class Twitter(Querier):
    '''
    Object used to query Twitter for ice-related tweets
    '''
    def __init__(self):
        pass

    def query(self):
        pass
        # auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        # auth.set_access_token(access_token, access_token_secret)
        #
        # api = tweepy.API(auth)
        #
        # public_tweets = api.home_timeline()
        # for tweet in public_tweets:
        #     print(tweet.text)

    def crawl(self):
        pass
