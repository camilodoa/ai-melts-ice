from datasetgenerator import Generator
from dateutil import relativedelta
import os.path
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.models import load_model
from tensorflow.keras.callbacks import History

class Learner():
    '''
    Predictor class. Used to build() and fit() a Keras LSTM model to
    make predictions of the future with predict(month, year).
    '''
    def __init__(self, t = 5, split = 0.70, epochs = 1000,
                neurons = 100,
                layers = [
                    Dense(200, activation = 'sigmoid'),
                    Dense(300, activation = 'relu'),
                    Dense(500, activation = 'sigmoid'),
                    LSTM(150, activation = 'relu')
                ], optimizer = 'adam', loss = 'mse', verbose = 0):
        '''
        Initialize class variables for network training
        '''
        # Initialize dataset generator class
        g = Generator()
        # Read in dataset into pandas DataFrame object
        df = pd.read_csv('data.csv', infer_datetime_format = True, parse_dates = ['Date'])
        # Sort values by date (earliest dates first)
        df = df.sort_values('Date').drop(['Date'], axis = 1)
        # Split into test and training
        self.split = split
        # Split remains the same among all Ai instances
        train, test = df.iloc[0:int(len(df) * self.split)], df.iloc[int(len(df) * self.split):len(df)]
        # Split dataset into X Y pairs
        self.X_train, self.Y_train = g.split(train, t)
        self.X_test, self.Y_test = g.split(test, t)
        # Define self.output_size layer size
        self.output_size = self.X_train.shape[2]
        # Parameters
        # Each prediction will be based on t data points before it
        self.t = t
        # How many epochs to train for
        self.epochs = epochs
        self.layers = layers
        self.neurons = neurons
        self.optimizer = 'adam'
        self.loss = 'mse'
        self.error = None
        self.verbose = verbose

    def build(self):
        '''
        Build a Keras LSTM network with three layers: LSTM, LSTM, Dense
        '''
        # Define the model
        self.model = Sequential()
        # Define the self.model's input's shape
        input_shape = (self.t, self.output_size)
        # Add the first LSTM layer with an input shape of t for each county
        self.model.add(LSTM(self.neurons, activation = 'relu', return_sequences = True, input_shape = input_shape))
        # Add customizable layers
        for layer in self.layers:
            self.model.add(layer)
        # Output layer
        self.model.add(Dense(self.output_size))
        # Compile the model
        self.model.compile(optimizer = self.optimizer, loss = self.loss)
        # Get description
        if self.verbose: self.model.summary()
        return self.model

    def fit(self, type = 'evaluation'):
        '''
        Fit the keras self.model
        '''
        # If model as already been fit, check that
        if self.error is not None:
            self.error = self.model.evaluate(self.X_test, self.Y_test, verbose=self.verbose) if type == 'evaluation' else self.history.history['loss'][-1]
            return self.error
        self.model = self.build()
        self.history = History()
        # Fit model
        self.history = self.model.fit(self.X_train, self.Y_train, epochs = self.epochs, callbacks=[self.history], verbose=self.verbose)
        # assign fitness
        self.error = self.model.evaluate(self.X_test, self.Y_test, verbose=self.verbose) if type == 'evaluation' else self.history.history['loss'][-1]
        return self.error

    def save(self, name):
        '''
        Save self.model
        '''
        self.model.save('models/{0}.h5'.format(name))
        print('Saved model to models/{0}.h5'.format(name))
        return self.model

    def predict_forward(self, month, year):
        '''
        Generate predictions until month year (greater than 2014) and write them to
        predictions.csv
        '''
        if os.path.isfile('model.h5'): self.model = load_model('model.h5')
        else: self.model = self.fit()
        # Load dataset
        df = pd.read_csv('data.csv', infer_datetime_format=True, parse_dates=['Date'])
        # Extract last recorded date
        date = pd.to_datetime(df['Date'].values[-1])
        # If the date predicted is in or before our dataset, do nothing
        if year < date.year: return None
        # Calculate difference between last date in dataset and the date given
        diff = (year - date.year) * 12 + month - date.month
        # Drop dates, they are not a part of the input of our NN self.model
        df.drop(['Date'], axis = 1)
        # Generate predictions for each month in difference
        g = Generator()
        for i in range(diff):
            # Convert last 12 months into data
            data = g.convert(df, self.t, -self.t, 0)
            # Use data to predict with the self.model
            predictions = self.model.predict(data)
            # Update current  date
            date = date + relativedelta(months = 1)
            # Only keep integer predictions - negative predictions are set to 0
            predictions = {city : int(round(max(prediction, 0))) for city, prediction in zip(df.columns, predictions[0])}
            # Append prediction to the predictions dataset (without date column)
            df = df.append(predictions, ignore_index = True)
            # Add date field to the prediction dictionary
            predictions.update({'Date' : date})
            # Append prediction dictionary with date to final DataFrame
            df = df.append(predictions, ignore_index = True)
        # Save data frame
        df.to_csv('predictions.csv', index = False)
        return predictions

    def genome(self):
        return {
            't' : self.t,
            'split' : self.split,
            'epochs' : self.epochs,
            'neurons' : self.neurons,
            'layers' : self.layers,
            'optimizer' : self.optimizer,
            'loss' : self.loss
        }

if __name__ == '__main__':
    'Usage'
    primis = Learner(verbose=1)
    primis.fit()
    # a.predict_forward(12, 2021)
