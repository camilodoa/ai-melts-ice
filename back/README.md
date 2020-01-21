# ai.melts.ice's backend

## getting started

`pip install -r requirements.txt` to download python dependencies

`python api.py` to start the REST API

please note that this was all written in python3


# about

`query.py` queries Syracuse's TRAC web API for information on ICE arrests by county

`datasetgenerator.py` uses the `Syracuse` class in `query.py` to create a dataset of ICE arrests in the US and saves it in `data.csv`

`ai.py` builds an LSTM model based on the dataset generated with `datasetgenerator.py`. It uses the model and dataset to predict future arrests and saves them in `predictions.csv`

`api.py` starts a RESTful API that serves the data in `predictions.csv`
