from datasetgenerator import Generator
from dateutil import relativedelta
import os.path
import pandas as pd
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
        self.n_steps = 12
        # Division between train and test
        self.split = 0.8
        train, test = df.loc[0:int(len(df) * self.split)], df.loc[int(len(df) * self.split):len(df)]
        # Split dataset into X Y pairs
        print('Splitting dataset into train and test (X, Y) pairs')
        self.X_train, self.Y_train = self.g.split(train, self.n_steps)
        self.X_test, self.Y_test = self.g.split(test, self.n_steps)
        # Define input layer shape
        self.input_shape = (self.X_train.shape[1], self.X_train.shape[2], self.X_train.shape[3],)
        print(self.input_shape)
        # Just output arrests
        self.output_shape = self.Y_train.shape[1]

    def build(self):
        '''
        Build a deep Keras LSTM network
        '''
        # Define the model
        model = Sequential()
        # Dense layer
        model.add(Dense(1000, activation = 'relu', return_sequences = True, input_shape = self.input_shape))
        # Add the first LSTM layer with an input shape of n_steps for each county
        model.add(LSTM(2000, activation = 'relu', return_sequences = True))
        # Dropout layer
        model.add(Dropout(0.2))
        # Dense layer
        model.add(Dense(1000, activation = 'relu'))
        # Add the second LSTM layer
        model.add(LSTM(1000, activation = 'relu'))
        # Dropout layer
        model.add(Dropout(0.2))
        # Dense layer
        model.add(Dense(2000, activation = 'relu'))
        # Dropout layer
        model.add(Dropout(0.2))
        # Add the final Dense layer
        model.add(Dense(self.output_shape))
        # Compile the model
        model.compile(optimizer = 'adam', loss = 'mse')
        # Print summary
        model.summary()
        return model

    def fit(self):
        '''
        Fit the model
        '''
        # Build model
        self.model = self.build()
        # Fit model
        self.history = self.model.fit(self.X_train, self.Y_train, epochs = 1000)
        self.error = self.model.evaluate(self.X_test, self.Y_test,
                verbose=1)
        print(self.error)
        # Save model
        self.model.save('models/model.h5')
        return self.error


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
