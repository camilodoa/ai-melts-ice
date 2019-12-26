import math
import numpy as np
import pandas as pd
import os.path
from datasetgenerator import Generator
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import RMSprop
from keras.callbacks import EarlyStopping
from keras.models import load_model

import matplotlib.pyplot as plt

class Predictor():

    def __init__(self):
        g = Generator()
        if g.reinit:
            g.initialize()

        df = pd.read_csv('data.csv')

        self.train = df.sample(frac = 0.8, random_state=0)

        self.train_X = self.train[['Year', 'Month']]
        self.train_Y = self.train.drop(['Year', 'Month'], axis=1)

        self.test = df.drop(self.train.index)
        self.test_X = self.test[['Year', 'Month']]
        self.test_Y = self.test.drop(['Year', 'Month'], axis=1)

        self.ready = False

    def build(self):
        model = Sequential([
            Dense(32, input_shape=[len(self.train_X.keys())], activation='relu'),
            Dense(64,  activation='relu'),
            Dense(128,  activation='relu'),
            Dense(len(self.train_Y.keys()))
        ])

        optimizer = RMSprop(0.001)

        model.compile(loss='mse', optimizer=optimizer, metrics=['mae', 'mse'])

        return model

    def fit(self):
        model = self.build()
        train = self.train.copy()

        early_stop = EarlyStopping(monitor='val_loss', patience=10)

        history = model.fit(self.train_X, self.train_Y,
                    epochs=1000, validation_split = 0.2, verbose=0,
                    callbacks=[early_stop])

        hist = pd.DataFrame(history.history)
        hist['epoch'] = history.epoch
        hist.tail()

        # plt.plot(hist[['epoch']], hist[['loss']])
        # plt.xlabel('epochs')
        # plt.ylabel('loss')
        # plt.show()
        #
        # plt.plot(hist[['epoch']], hist[['mae']])
        # plt.xlabel('epochs')
        # plt.ylabel('mae')
        # plt.show()
        #
        # plt.plot(hist[['epoch']], hist[['mse']])
        # plt.xlabel('epochs')
        # plt.ylabel('mse')
        # plt.show()

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
            else:
                self.fit()

        predictions = self.model.predict(np.array([[year , month]]))

        predictions = {city : prediction for city, prediction in zip(self.train.columns, predictions[0])}

        print(predictions)

        return predictions


if __name__ == '__main__':
    p = Predictor()
    p.fit()
    p.predict(2019, 11)
