from keras.callbacks import EarlyStopping
from datasetgenerator import Generator
from dateutil.relativedelta import *
from keras.layers import Dense, LSTM
from keras.models import Sequential
from keras.models import load_model
import pandas as pd
import os.path

class Predictor():
    '''
    Predictor class. Used to build() and fit() a Keras LSTM model to
    make predictions of the future with predict(month, year).
    '''

    def __init__(self):

        g = Generator()
        if g.reinit:
            g.initialize()

        df = pd.read_csv('data.csv', infer_datetime_format = True,
            parse_dates = ['Date'])

        df = df.sort_values('Date').drop(['Date'], axis = 1)

        self.n_steps = 12
        self.X, self.Y = g.split(df, self.n_steps)

        self.n_features = self.X.shape[2]

        self.ready = False


    def build(self):

        model = Sequential()
        model.add(LSTM(100, activation = 'relu', return_sequences = True,
            input_shape = (self.n_steps, self.n_features)))
        model.add(LSTM(200, activation = 'relu'))
        model.add(Dense(self.n_features))

        model.compile(optimizer = 'adam', loss = 'mse')

        return model


    def fit(self):

        model = self.build()

        early_stop = EarlyStopping(monitor='val_loss', patience=10)

        history = model.fit(self.X, self.Y, epochs = 1000, callbacks=[early_stop])

        self.model = model
        model.save('model.h5')

        self.ready = True

        return model


    def predict(self, month, year):
        '''
        Make predictions until month year (greater than 2014) and write that to
        predictions.csv
        '''

        if os.path.isfile('model.h5'):
            self.model = model = load_model('model.h5')
            self.ready = True
        else:
            model = self.fit()

        g = Generator()

        df = pd.read_csv('data.csv', infer_datetime_format=True,
            parse_dates=['Date'])

        predictions_df = df.drop(['Date'], axis = 1)

        # Extract last recorded date
        date = pd.to_datetime(df['Date'].values[-1])

        if year < date.year: return None

        diff = (year - date.year) * 12 + month - date.month

        for i in range(diff):
            data = g.convert(predictions_df, self.n_steps, -self.n_steps, 0)

            predictions = model.predict(data)

            date = date + relativedelta(months = 1)

            # Only keep integer predictions; negative predictions should be set to 0
            predictions = {city : int( round( max(prediction, 0) ) ) for city, prediction in zip(predictions_df.columns, predictions[0])}

            predictions_df = predictions_df.append(predictions, ignore_index = True)

            predictions.update({'Date' : date})

            df = df.append(predictions, ignore_index = True)

        df.to_csv('predictions.csv', index = False)

        return predictions
        

if __name__ == '__main__':
    'Usage'
    p = Predictor()
    p.predict(12, 2021)
