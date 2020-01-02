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
        self.cities = 385
        self.counties = 1972

    def query(self, county):
        url = (
            'https://trac.syr.edu/phptools/immigration/arrest/graph.php?stat='
            'count&timescale=fymon&county=[COUNTY]&timeunit=number'
        ).replace('[COUNTY]', county)

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
