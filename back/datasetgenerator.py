from geopy.geocoders import Nominatim
import pandas as pd
import numpy as np
import pickle
import time
import requests
import urllib.request as urllib

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

class Census():
    '''
    Object used to query US Gov't census dataset

    Website: https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/counties/totals/
    '''
    def __init__(self):
        self.link = 'https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/counties/totals/co-est2019-alldata.csv'

    def download_population(self):
        data = urllib.urlopen(self.link)
        data = data.read()
        with open('./population2010-2019.csv', 'wb') as f:
            f.write(data)

    def save_state_codes(self):
        mapping = {
            'Armed Forces America' : 'AA',
            'Armed Forces' : 'AE',
            'Alaska' : 'AK',
            'Alabama' : 'AL',
            'Armed Forces Pacific' : 'AP',
            'Arkansas' : 'AR',
            'Arizona' : 'AZ',
            'California' : 'CA',
            'Colorado' : 'CO',
            'Connecticut' : 'CT',
            'Washington DC' : 'DC',
            'Delaware' : 'DE',
            'Florida' : 'FL',
            'Georgia' : 'GA',
            'Guam' : 'GU',
            'Hawaii' : 'HI',
            'Iowa' : 'IA',
            'Idaho' : 'ID',
            'Illinois' : 'IL',
            'Indiana' : 'IN',
            'Kansas' : 'KS',
            'Kentucky' : 'KY',
            'Louisiana' : 'LA',
            'Massachusetts' : 'MA',
            'Maryland' : 'MD',
            'Maine' : 'ME',
            'Michigan' : 'MI',
            'Minnesota' : 'MN',
            'Missouri' : 'MO',
            'Mississippi' : 'MS',
            'Montana' : 'MT',
            'North Carolina' : 'NC',
            'North Dakota' : 'ND',
            'Nebraska' : 'NE',
            'New Hampshire' : 'NH',
            'New Jersey' : 'NJ',
            'New Mexico' : 'NM',
            'Nevada' : 'NV',
            'New York' : 'NY',
            'Ohio' : 'OH',
            'Oklahoma' : 'OK',
            'Oregon' : 'OR',
            'Pennsylvania' : 'PA',
            'Puerto Rico' : 'PR',
            'Rhode Island' : 'RI',
            'South Carolina' : 'SC',
            'South Dakota' : 'SD',
            'Tennessee' : 'TN',
            'Texas' : 'TX',
            'Utah' : 'UT',
            'Virginia' : 'VA',
            'Virgin Islands' : 'VI',
            'Vermont' : 'VT',
            'Washington' : 'WA',
            'Wisconsin' : 'WI',
            'West Virginia' : 'WV',
            'Wyoming' : 'WY'
        }
        pickle.dump(mapping,open( 'states.dict', 'wb' ))
        return mapping

    def load_state_codes(self):
        return pickle.load(open('states.dict','rb'))

class Generator():
    '''
    Generator class. Used to initialize() an ICE arrests dataset by querying
    the Syracuse TRAC web API.
    '''
    def __init__(self, reinit = False, reinit_locations = False):
        # Reinitialize dataset (T/F)
        self.reinit = reinit
        self.reinit_locations = reinit_locations
        self.s = Syracuse()
        self.c = Census()
        self.initialize()

    def initialize(self):
            '''
            Initializes and saves Syracuse data to file (arrests2014-2018.csv)
            '''
            if not self.reinit: return
            ok = ''

            # Reinit ICE data?
            while ok != 'y' and ok != 'n':
                ok = input('Download arrests2014-2018.csv? Y/N: ').lower().strip()
            if ok.lower() == 'n': pass
            elif ok.lower() == 'y': self.download_arrests().to_csv('arrests2014-2018.csv', index = False)

            # Reinit county to location data
            # This is a costly operation, so there is a seperate check for it
            if self.reinit_locations: self.download_locations()

            # Reinit population data?
            ok = ''
            while ok != 'y' and ok != 'n':
                ok = input('Download population2010-2019.csv? Y/N: ').lower().strip()
            if ok.lower() == 'n': pass
            elif ok.lower() == 'y':
                c = Census()
                c.download_population()

            # Reinit dataset?
            ok = ''
            while ok != 'y' and ok != 'n':
                ok = input('Create dataset.csv? Y/N: ').lower().strip()
            if ok.lower() == 'n': pass
            elif ok.lower() == 'y':
                self.create_dataset().to_csv('dataset.csv', index = False)
                self.save_segmented_dataset()

    def fetch_arrests(self, county):
        '''
        Queries Syracuse DB for data on a particular county, based on #
        '''
        return self.s.query(str(county))

    def download_arrests(self):
        '''
        Fills out empty Pandas DF with Syracuse data
        '''
        df = pd.DataFrame()
        # Create dictionary to make the transition to dataset easier
        dict = {}
        for county in range(self.s.counties):
            json = self.fetch_arrests(county)
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

    def download_locations(self):
        '''
        Make and save a dictionary for translating county name to coordinate
        '''
        df = self.load_arrests().drop(['Date'], axis = 1)
        geolocator, mapping = Nominatim(user_agent='ai-melts-ice', timeout=None), {}
        for i, county in enumerate(df.columns):
            location = geolocator.geocode(county)
            mapping.update({county : [location.latitude, location.longitude]})
            print(i, {county : [location.longitude, location.latitude]})
            # Don't spam their servers too much
            time.sleep(1)
        pickle.dump(mapping,open( 'coordinates.dict', 'wb' ))
        return mapping

    def create_dataset(self):
        '''
        Used to create a dataset with arrest, population, and location data
        for training
        '''
        population = self.load_population()
        states = self.c.load_state_codes()
        locations = self.load_locations()
        arrests = self.load_arrests()

        # Load population and dates that we care about
        population = population.filter(
            items=['CTYNAME', 'POPESTIMATE2014', 'POPESTIMATE2015',
            'POPESTIMATE2016', 'POPESTIMATE2017', 'POPESTIMATE2018',
            'POPESTIMATE2019']
        )

        # Match population counties to dataset counties
        curr_code = None
        for i in population.index:
            # Current county
            curr = population.loc[i, 'CTYNAME']
            # County name attempted to be converted to state code
            state = states.get(curr)
            # Special case
            if curr == 'District of Columbia':
                population.loc[i, 'CTYNAME'] = 'District of Columbia, DC'
                continue
            # If the current county name is a state name, that will be the state
            # the next counties are in
            if state != None:
                # Set the current code to the state code
                curr_code = state
            # If the current county is not a state, rename it using the
            # last found state code
            elif curr_code != None:
                population.loc[i, 'CTYNAME'] = curr + ', ' + curr_code

        # Find values in ICE dataset that aren't in population dataset
        missing = []
        for key, value in locations.items():
            if not (population['CTYNAME'] == key).any():
                missing.append(key)

        # Filter rows based on whether they're in ICE dataset
        population = population[population['CTYNAME'].map(lambda x : locations.get(x) is not None)]
        # Drop values in ICE dataset that aren't in population dataset
        arrests = arrests.drop(columns=missing, axis = 1)

        # Create new dataset for ML
        no_date = arrests.drop(['Date'], axis=1)
        labels = ['{0} - arrests', '{0} - population', '{0} - longitude', '{0} - latitude']
        new_columns = [label.format(county) for county in no_date.columns for label in labels]
        new_columns.append('Date')
        dataset = pd.DataFrame(index=arrests.index, columns=new_columns)

        # Populate dataset
        for i in arrests.index:
            year = arrests.loc[i, 'Date'][-2:]
            dataset.loc[i, 'Date'] = arrests.loc[i, 'Date']
            for j in population.index:
                # Retrieve data
                county = population.loc[j, 'CTYNAME']
                pop = population.loc[j, 'POPESTIMATE20' + year]
                arr = arrests.loc[i, county]
                longitude = locations.get(county)[0]
                latitude = locations.get(county)[1]
                # Fill in new dataset
                dataset.loc[i, labels[0].format(county)] = arr
                dataset.loc[i, labels[1].format(county)] = pop
                dataset.loc[i, labels[2].format(county)] = longitude
                dataset.loc[i, labels[3].format(county)] = latitude

        return dataset

    def load_locations(self):
        return pickle.load(open('coordinates.dict','rb'))

    def load_arrests(self):
        return pd.read_csv('arrests2014-2018.csv', encoding = 'utf8')

    def load_population(self):
        return pd.read_csv('population2010-2019.csv', encoding = 'ISO-8859-1')

    def load_dataset(self, parse_dates = False):
        return pd.read_csv('dataset.csv', infer_datetime_format=True, parse_dates=['Date']) if parse_dates else pd.read_csv('dataset.csv', encoding = 'utf8')

    def split(self, df, n_steps):
        '''
        Splits data frame into X Y pairs for network.
        n_steps is the number of months in each X.
        '''

        n = len(df.values)
        # Arrange our input into groups of 4 datapoints per county
        sequences_x = []
        for i in range(n):
            j = 0
            m = len(df.columns)
            curr = []
            while j < m:
                curr.append(df.iloc[i, j : j + 4].values)
                j += 4
            sequences_x.append(curr)
        sequences_x = np.array(sequences_x)

        # Arrange our output to only contain arrests per county
        y_columns = [col for col in df.columns if 'arrests' in col]
        sequences_y = df[y_columns].values

        X, Y = [], []
        for k in range(n):
            # End of pattern
            end_ix = k + n_steps
            # Check for out of bounds exceptions
            if end_ix > len(sequences_x) - 1: break
            # Input and output parts of the pattern
            seq_x, seq_y = sequences_x[k : end_ix, :], sequences_y[end_ix, :]
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

if __name__ == '__main__':
    'Usage'
    g = Generator(reinit = False)
