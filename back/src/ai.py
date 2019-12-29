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

        df = pd.read_csv('data.csv', infer_datetime_format=True, parse_dates=['Date']).drop(['Date'], axis=1)

        print(df.values)
        data = df.values
        r, c = data.shape
        data = data.reshape(1, r, c)

        self.train = df.sample(frac = 0.8, random_state=0)

        self.train_X = self.train.drop(['Removals'], axis=1)
        self.train_Y = self.train[['Removals']]

        self.test = df.drop(self.train.index)
        self.test_X = self.test.drop(['Removals'], axis=1)
        self.test_Y = self.test[['Removals']]

        self.ready = False

    def build(self):

        model = Sequential()
        model.add(LSTM(256, input_shape=[len(self.train_X.keys())], return_sequences=True))
        model.add(Dropout(0.5))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(16, activation='relu'))
        model.add(Dense(len(self.train_y.keys()), activation='sigmoid'))

        optimizer = RMSprop(lr=lr)

        model.compile(loss='mean_squared_error', optimizer=optimizer)

        return model

    def fit(self):

        model = self.build()
        train = self.train.copy()

        history = model.fit(self.train_X, self.train_Y,
                    epochs=1000, validation_split = 0.2)

        hist = pd.DataFrame(history.history)
        hist['epoch'] = history.epoch
        hist.tail()

        plt.plot(hist[['epoch']], hist[['loss']])
        plt.xlabel('epochs')
        plt.ylabel('loss')
        plt.show()

        plt.plot(hist[['epoch']], hist[['mae']])
        plt.xlabel('epochs')
        plt.ylabel('mae')
        plt.show()

        plt.plot(hist[['epoch']], hist[['mse']])
        plt.xlabel('epochs')
        plt.ylabel('mse')
        plt.show()

        loss, mae, mse = model.evaluate(self.test_X, self.test_Y)

        print("Testing set Mean Abs Error: {:5.2f} MPG".format(mae))

        self.ready = True
        self.model = model

        model.save('model.h5')

        return model, hist

    def predict(self, year, month):

        if not self.ready:
            if os.path.isfile('model.h5'):
                self.model = load_model('model.h5')
                self.ready = True
            else:
                self.fit()

        predictions = self.model.predict(np.array([[year , month]]))

        predictions = {city : prediction for city, prediction in zip(self.train.columns, predictions[0])}

        print(predictions)

        return predictions


if __name__ == '__main__':
    p = Predictor()
    p.fit()
    # p.predict(2019, 11)
