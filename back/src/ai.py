import math
import numpy as np
import pandas as pd
import os.path
from datasetgenerator import Generator
from keras.models import Sequential
from keras.layers import Dense, Dropout, Embedding, LSTM, Bidirectional
from keras.optimizers import RMSprop
from keras.callbacks import EarlyStopping
from keras.models import load_model

import matplotlib.pyplot as plt

class Predictor():

    def __init__(self):
        g = Generator()
        if g.reinit:
            g.initialize()

        df = pd.read_csv('data.csv', infer_datetime_format=True, parse_dates=['Date']).drop(['Date'], axis = 1)

        train, test = g.split(df)

        self.look_back = 1
        self.trainX, self.trainY = g.LSTM_convert(train, self.look_back)
        self.testX, self.testY = g.LSTM_convert(test, self.look_back)

        self.ready = False

    def build(self):

        model = Sequential()
        model.add(Dense(8, input_dim=self.look_back, activation='relu'))
        model.add(Dense(1))
        model.compile(loss='mean_squared_error', optimizer='adam')

        return model

    def fit(self):

        model = self.build()

        history = model.fit(self.trainX, self.trainY, epochs=200, batch_size=2, verbose=2)

        train_score = model.evaluate(self.trainX, self.trainY, verbose=0)
        print('Train Score: %.2f MSE (%.2f RMSE)' % (train_score, math.sqrt(train_score)))
        test_score = model.evaluate(self.testX, self.testY, verbose=0)
        print('Test Score: %.2f MSE (%.2f RMSE)' % (test_score, math.sqrt(test_score)))

        self.model = model
        model.save('model.h5')

        self.ready = True

        return model, history

    def predict(self, year, month):

        if not self.ready:
            if os.path.isfile('model.h5'):
                self.model = model = load_model('model.h5')
                self.ready = True
            else:
                model, history = self.fit()


        predictions = self.model.predict(np.array([[year , month]]))

        predictions = {city : prediction for city, prediction in zip(self.train.columns, predictions[0])}

        print(predictions)

        return predictions


if __name__ == '__main__':
    p = Predictor()
    p.fit()
    p.predict(2019, 11)
