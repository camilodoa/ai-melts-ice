from datasetgenerator import Generator
from dateutil import relativedelta
import os.path
import sys
import pandas as pd
import random

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.models import load_model

class Model():
    '''
    Predictor class. Used to build() and fit() a Keras LSTM model to
    make predictions of the future with predict(month, year).
    '''

    def __init__(self):
        '''
        Initialize class variables for network training
        '''
        # Initialize dataset generator class
        print('Initializing dataset')
        self.g = Generator()
        # Read in dataset into pandas DataFrame object
        df = self.g.load_dataset(parse_dates = True)
        # Sort values by date (earliest dates first)
        df = df.sort_values('Date').drop(['Date'], axis = 1)
        # Each prediction will be based on n_steps data points before it
        self.n_steps = 2
        # Division between train and test
        self.split = 0.8
        train, test = df.iloc[0:int(len(df) * self.split)], df.iloc[int(len(df) * self.split):len(df)]
        # Split dataset into X Y pairs
        print('Splitting dataset into train and test (X, Y) pairs')
        self.X_train, self.Y_train = self.g.split(train, self.n_steps)
        self.X_test, self.Y_test = self.g.split(test, self.n_steps)
        # Define input layer shape
        self.input_shape = (self.X_train.shape[1], self.X_train.shape[2])
        # Just output arrests
        self.output_shape = self.Y_train.shape[1]
        # Name array
        self.names = []
        with open('names.txt', 'r') as f:
            for line in f:
                for name in line.split():
                    self.names.append(name)

    def build(self):
        '''
        Build a deep Keras LSTM network
        '''
        # Define the model
        model = Sequential()
        # Add the first LSTM layer with an input shape of n_steps for each county
        model.add(LSTM(8000, activation = 'tanh', recurrent_activation="sigmoid",return_sequences = True, input_shape = self.input_shape))
        model.add(Dropout(0.2))

        model.add(Dense(7000, activation = 'relu'))
        model.add(Dropout(0.2))

        model.add(Dense(6000, activation = 'relu'))
        model.add(Dropout(0.2))

        model.add(Dense(5000, activation = 'relu'))
        model.add(Dropout(0.2))

        model.add(Dense(4000, activation = 'relu'))
        model.add(Dropout(0.2))

        model.add(Dense(3000, activation = 'relu'))
        model.add(Dropout(0.2))

        model.add(Dense(2000, activation = 'relu'))
        model.add(Dropout(0.2))

        model.add(Dense(2000, activation = 'relu'))
        model.add(Dropout(0.2))

        model.add(LSTM(2000, activation = 'tanh', recurrent_activation="sigmoid"))
        model.add(Dropout(0.2))

        # Output lauer
        model.add(Dense(self.output_shape))
        # Compile the model
        model.compile(optimizer = 'adam', loss = 'mse', metrics=['accuracy'],
            validation_split=0.33, epochs=800)
        # Print summary
        model.summary()
        return model

    def fit(self):
        '''
        Fit the model
        '''
        # Build model
        self.model = self.build()
        # Early Stopping
        # callback = EarlyStopping(monitor='loss', patience=10, mode='min')
        # Fit model
        self.history = self.model.fit(self.X_train, self.Y_train, epochs = 500,
            batch_size = 32, verbose = 1)

        print(history.history['loss'])
        print(history.history['accuracy'])
        print(history.history['val_loss'])
        print(history.history['val_accuracy'])

        try:
            self.error = self.model.evaluate(self.X_test, self.Y_test)
        except:
            e = sys.exc_info()[0]
            write_to_page( "<p>Error: %s</p>" % e )

        self.error = self.history.history['loss'][-1]
        print(self.error)
        self.save()
        return self.error

    def save(self):
        name = random.choice(self.names) + str(int(self.error))
        self.model.save('models/{0}.h5'.format(name))
        return name


    def predict_forward(self, month, year):
        '''
        Generate predictions until month year (greater than 2014) and write them to
        predictions.csv
        '''
        if os.path.isfile('model.h5'): model = load_model('model.h5')
        else: model = self.fit()
        # Load dataset
        df = self.g.load_dataset(parse_dates = True)
        # Extract last recorded date
        date = pd.to_datetime(df['Date'].values[-1])
        # If the date predicted is in or before our dataset, do nothing
        if year < date.year: return None
        # Calculate difference between last date in dataset and the date given
        diff = (year - date.year) * 12 + month - date.month
        # Drop dates, they are not a part of the input of our NN model
        df.drop(['Date'], axis = 1)
        # Generate predictions for each month in difference
        for i in range(diff):
            # Convert last 12 months into data
            data = self.g.convert(df, self.n_steps, -self.n_steps, 0)
            # Use data to predict with the model
            predictions = model.predict(data)
            # Update current prediction date
            date = date + relativedelta(months = 1)
            # Only keep integer predictions - negative predictions are set to 0
            predictions = {city : int( round( max(prediction, 0) ) ) for city, prediction in zip(df.columns, predictions[0])}
            # Append prediction to the predictions dataset (without date column)
            df = df.append(predictions, ignore_index = True)
            # Add date field to the prediction dictionary
            predictions.update({'Date' : date})
            # Append prediction dictionary with date to final DataFrame
            df = df.append(predictions, ignore_index = True)
        # Save data frame
        df.to_csv('predictions.csv', index = False)
        return predictions

if __name__ == '__main__':
    'Usage'
    a = Model()
    a.fit()
    # a.predict_forward(12, 2021)
