import requests

'''
Contains the classes used for querying APIs that have information on ICE
'''
class Syracuse():
    '''
    Object used to query Syracuse deportation database

    Website: https://trac.syr.edu/phptools/immigration/arrest/
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
        return requests.get(url, headers=headers).json()