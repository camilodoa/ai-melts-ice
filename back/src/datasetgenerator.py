import pandas as pd
import numpy as np
from query import Syracuse

class Generator():
    '''
    Generator class. Used to initialize() an ICE arrests dataset by querying
    the Syracuse TRAC web API.
    '''

    def __init__(self):
        # Reinitialize dataset (T/F)
        self.reinit = False


    def fetch(self, county):
        'Queries Syracuse DB for data on a particular county, based on #'

        s = Syracuse()
        return s.query(str(county))


    def fill(self):
        'Fills out empty Pandas DF with Syracuse data'

        s = Syracuse()
        df = pd.DataFrame()

        'Create dictionary to make the transition to dataset easier'
        dict = {}

        for county in range(s.counties):
            json = self.fetch(county)
            print(json['title'])

            if json['title'] == '':
                continue

            for point in json['timeline']:
                date = pd.to_datetime(point['fymon'])
                county = json['title']

                if dict.get(date) == None:
                    dict[date] = {'Date' : date}

                dict[date][county] = int(point['number'])

        'Transfer dictionary layout to dataset'
        for data in dict.values():
            df = df.append(data, ignore_index = True, sort = False)

        df = df.fillna(0)
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values(by = ['Date'])

        return df


    def initialize(self):
        'Initializes and saves Syracuse data to file (data.csv)'

        df = self.fill()

        ok = ''
        while ok != 'y' and ok != 'n':
            ok = input('Overwrite data.csv? Y/N: ').lower().strip()

        if ok.lower() == 'n':
            return None

        df.to_csv('data.csv', index = False)

        return df


    def split(self, df, n_steps):
        'Splits dataset into X Y pairs for network'

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
        'Converts dataset into X input for network'
        
        sequences = df.values

        X = []

        if hi == 0: X.append(sequences[lo:, :])
        else: X.append(sequences[lo:hi, :])

        return np.array(X)


if __name__ == '__main__':
    'Usage'
    g = Generator()
    g.initialize()
