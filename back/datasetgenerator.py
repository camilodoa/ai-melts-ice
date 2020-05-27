from geopy.geocoders import Nominatim
import pandas as pd
import numpy as np
import pickle
import time
import requests

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

class Generator():
    '''
    Generator class. Used to initialize() an ICE arrests dataset by querying
    the Syracuse TRAC web API.
    '''
    def __init__(self):
        # Reinitialize dataset (T/F)
        self.reinit = False
        self.make_mapping = False

    def initialize(self):
            '''
            Initializes and saves Syracuse data to file (data.csv)
            '''
            if not self.reinit: return
            df, ok = self.fill(), ''
            while ok != 'y' and ok != 'n':
                ok = input('Overwrite data.csv? Y/N: ').lower().strip()
            # Exit
            if ok.lower() == 'n': return None
            # load database
            df.to_csv('data.csv', index = False)
            # prepare
            if self.make_mapping: self.prep_mapping()
            return df

    def fetch(self, county):
        '''
        Queries Syracuse DB for data on a particular county, based on #
        '''
        s = Syracuse()
        return s.query(str(county))

    def fill(self):
        '''
        Fills out empty Pandas DF with Syracuse data
        '''
        s = Syracuse()
        df = pd.DataFrame()
        # Create dictionary to make the transition to dataset easier
        dict = {}
        for county in range(s.counties):
            json = self.fetch(county)
            print(json['title'])
            if json['title'] == '': continue
            for point in json['timeline']:
                date = pd.to_datetime(point['fymon'])
                county = json['title']
                if dict.get(date) == None: dict[date] = {'Date' : date}
                dict[date][county] = int(point['number'])
        # Transfer dictionary layout to dataset
        for data in dict.values():
            df = df.append(data, ignore_index = True, sort = False)
        df = df.fillna(0)
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values(by = ['Date'])
        return df

    def split(self, df, n_steps):
        '''
        Splits data frame into X Y pairs for network.
        n_steps is the number of months in each X.
        '''
        sequences = df.values
        X, Y = [], []
        for i in range(len(sequences)):
            # End of pattern
            end_ix = i + n_steps
            # Check for out of bounds exceptions
            if end_ix > len(sequences)-1: break
            # Input and output parts of the pattern
            seq_x, seq_y = sequences[i:end_ix, :], sequences[end_ix, :]
            X.append(seq_x)
            Y.append(seq_y)
        return np.array(X), np.array(Y)

    def convert(self, df, n_steps, lo, hi):
        '''
        Converts table tuple into X input for network
        '''
        sequences = df.values
        X = []
        if hi == 0: X.append(sequences[lo:, :])
        else: X.append(sequences[lo:hi, :])
        return np.array(X)

    def prep_mapping(self):
        '''
        Make and save a dictionary for translating county name to coordinate
        '''
        df = pd.read_csv('data.csv', encoding = 'utf8').drop(['Date'], axis = 1)
        geolocator, mapping = Nominatim(user_agent="ai-melts-ice", timeout=None), {}
        for i, county in enumerate(df.columns):
            location = geolocator.geocode(county)
            mapping.update({county : [location.latitude, location.longitude]})
            print(i, {county : [location.longitude, location.latitude]})
            # Don't spam their servers too much
            time.sleep(1)
        return self.save_mapping(mapping)

    def save_mapping(self, mapping):
        pickle.dump(mapping,open( "coordinates.dict", "wb" ))
        return mapping

    def load_mapping(self):
        return pickle.load(open("coordinates.dict","rb"))


if __name__ == '__main__':
    'Usage'
    g = Generator()
    g.reinit = True
    g.initialize()
