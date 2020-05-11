from datasetgenerator import Generator
from dateutil import relativedelta
import os.path
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.models import load_model

class Ai():
    '''
    Predictor class. Used to build() and fit() a Keras LSTM model to
    make predictions of the future with predict(month, year).
    '''

    def __init__(self):
        '''
        Initialize class variables for network training
        '''
        # Initialize dataset generator class
        g = Generator()
        # Based on generator configurations, initialize a new dataset
        if g.reinit:
            g.initialize()
        # Read in dataset into pandas DataFrame object
        df = pd.read_csv('data.csv', infer_datetime_format = True, parse_dates = ['Date'])
        # Sort values by date (earliest dates first)
        df = df.sort_values('Date').drop(['Date'], axis = 1)
        # Each prediction will be based on n_steps data points before it
        self.n_steps = 12
        # Split dataset into X Y pairs
        self.X, self.Y = g.split(df, self.n_steps)
        # Define output layer size
        self.n_features = self.X.shape[2]

    def build(self):
        '''
        Build a Keras LSTM network with three layers: LSTM, LSTM, Dense
        '''
        # Define the model
        model = Sequential()
        # Define the model's input's shape
        input_shape = (self.n_steps, self.n_features)
        # Add the first LSTM layer with an input shape of n_steps for each county
        model.add(LSTM(100, activation = 'relu', return_sequences = True, input_shape = input_shape))
        # Add the second LSTM layer
        model.add(LSTM(200, activation = 'relu'))
        # Add the final Dense layer
        model.add(Dense(self.n_features))
        # Compile the model
        model.compile(optimizer = 'adam', loss = 'mse')
        return model

    def fit(self):
        '''
        Fit the keras model
        '''
        # Build model
        model = self.build()
        # Fit model
        history = model.fit(self.X, self.Y, epochs = 1000)
        print(history)
        # Save model
        model.save('model.h5')
        return model


    def predict_forward(self, month, year):
        '''
        Generate predictions until month year (greater than 2014) and write them to
        predictions.csv
        '''
        if os.path.isfile('model.h5'): model = load_model('model.h5')
        else: model = self.fit()
        # Load dataset
        df = pd.read_csv('data.csv', infer_datetime_format=True, parse_dates=['Date'])
        # Extract last recorded date
        date = pd.to_datetime(df['Date'].values[-1])
        # If the date predicted is in or before our dataset, do nothing
        if year < date.year: return None
        # Calculate difference between last date in dataset and the date given
        diff = (year - date.year) * 12 + month - date.month
        # Drop dates, they are not a part of the input of our NN model
        df.drop(['Date'], axis = 1)
        # Generate predictions for each month in difference
        g = Generator()
        for i in range(diff):
            # Convert last 12 months into data
            data = g.convert(df, self.n_steps, -self.n_steps, 0)
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
    a = Ai()
    a.fit()
    # a.predict_forward(12, 2021)

