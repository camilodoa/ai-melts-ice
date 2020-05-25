from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.models import load_model
from tensorflow.keras.callbacks import History
from datasetgenerator import Generator
from dateutil import relativedelta
import os.path
import pandas as pd
import pickle
from progress.bar import Bar


class Model():
    '''
    Model class. Used to build() and fit() a Keras LSTM model to
    make predictions of the future with predict(month, year).
    Serialized with genome.
    Takes in customizable arguments of serialization.
    Also takes in the path to a time-series Pandas dataset, with an attribute
    labeled "Date".
    '''
    def __init__(self, t = 12, split = 0.70, epochs = 1000,
                neurons = 100,
                layers = [
                    LSTM(200)
                ], optimizer = 'adam', loss = 'mse', verbose = 0,
                dataset='data.csv'):
        '''
        Initialize class variables for network training
        '''
        # Initialize dataset generator class
        g = Generator()
        self.dataset = dataset
        # Read in dataset into pandas DataFrame object
        df = pd.read_csv(dataset, infer_datetime_format = True, parse_dates = ['Date'])
        # Sort values by date (earliest dates first)
        df = df.sort_values('Date').drop(['Date'], axis = 1)
        self.final = split == 1
        if self.final:
            self.split = 1
            train = df.iloc[:]
            # Split dataset into X Y pairs
            self.X_train, self.Y_train = g.split(train, t)
        else:
            # Split into test and training
            self.split = split
            # Split
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
        self.optimizer = optimizer
        self.loss = loss
        self.error = None
        self.verbose = verbose
        self.model = None

    def build(self):
        '''
        Build a Keras LSTM network with three layers: LSTM, LSTM, Dense
        '''
        if self.verbose: bar = Bar('Building model', fill='=', max=len(self.layers) + 2)

        # Define the model
        self.model = Sequential()
        # Define the self.model's input's shape
        input_shape = (self.t, self.output_size)
        # Add the first LSTM layer with an input shape of t for each county
        self.model.add(LSTM(self.neurons, return_sequences = True, input_shape = input_shape))
        if self.verbose: bar.next()
        # Add customizable layers
        for layer in self.layers:
            self.model.add(layer)
            if self.verbose: bar.next()
        # Output layer
        self.model.add(Dense(self.output_size))
        if self.verbose: bar.next()
        # Compile the model
        self.model.compile(optimizer = self.optimizer, loss = self.loss)
        if self.verbose: bar.finish()
        # Get description
        if self.verbose: self.model.summary()
        return self.model

    def fit(self, type = 'evaluation'):
        '''
        Fit the keras self.model
        '''
        # If model as already been fit, check that
        if self.error is not None: return self.error
        if self.model is None: self.model = self.build()
        self.history = History()
        self.history = self.model.fit(self.X_train, self.Y_train,
            epochs = self.epochs, callbacks=[self.history], verbose=self.verbose)
        # Assign fitness
        if self.final:
            self.error = self.history.history['loss'][-1]
        else:
            self.error = self.model.evaluate(self.X_test, self.Y_test,
                verbose=self.verbose) if type == 'evaluation' else self.history.history['loss'][-1]
        return self.error

    def save(self, name = 'model'):
        '''
        Save self.model and genome serialization
        '''
        self.model.save('models/{0}.h5'.format(name))
        print('Saved model to models/{0}.h5'.format(name))

        with open('individuals/{0}.genome'.format(name), 'wb') as output:
            genome = self.get_genome()
            genome.pop('layers') # Remove layers because they can't be serialized
            pickle.dump(genome, output, -1)
            print('Saved individual to individuals/{0}.genome'.format(name))
        return self.model

    def predict(self, month, year):
        '''
        Generate predictions until month year (greater than 2014) and write them to
        predictions.csv
        '''
        g = Generator()
        # Load dataset
        df = pd.read_csv(self.dataset, infer_datetime_format=True,
            parse_dates=['Date'])
        # Drop dates, they are not a part of the input of our NN model
        predictions_df = df.drop(['Date'], axis = 1)
        # Extract last recorded date
        date = pd.to_datetime(df['Date'].values[-1])
        # If the date predicted is in or before our dataset, do nothing
        if year < date.year: return None
        # Calculate difference between last date in dataset and the date given
        diff = (year - date.year) * 12 + month - date.month
        if self.verbose: bar = Bar('Predicting months since ' + str(date), fill='=', max=diff)
        # Generate predictions for each month in difference
        for i in range(diff):
            # Convert last 12 months into data
            data = g.convert(predictions_df, self.t, -self.t, 0)
            # Use data to predict with the model
            predictions = self.model.predict(data)
            # Update current prediction date
            date = date + relativedelta.relativedelta(months = 1)
            # Make a dictionary of {cities : predicted arrests}
            predictions = {city : int(round(prediction)) for city, prediction in zip(predictions_df.columns, predictions[0])}
            # Append prediction to the predictions dataset (without date column)
            predictions_df = predictions_df.append(predictions, ignore_index = True)
            # Add date field to the prediction dictionary
            predictions.update({'Date' : date})
            # Append prediction dictionary with date to final DataFrame
            df = df.append(predictions, ignore_index = True)
            if self.verbose: bar.next()
        if self.verbose: bar.finish()
        dates = df.pop('Date')
        df = df.clip(lower = 0, axis = 1)
        df['Date'] = dates
        # Save dataframe
        df.to_csv('predictions.csv', index = False)
        return predictions

    def get_genome(self):
        return { 't' : self.t, 'split' : self.split, 'epochs' : self.epochs,
            'neurons' : self.neurons, 'layers' : self.layers,
            'optimizer' : self.optimizer,'loss' : self.loss}

if __name__ == '__main__':
    'Usage'
    primis = Model(verbose=1)
    primis.fit()
    # a.predict_forward(12, 2021)
