# ai.melts.ice

## about

ai.melts.ice is a web app designed to source and visualize predictions of ICE arrests in the US. These predictions are generated by an LSTM trained on ICE arrest data (2014 - 2018) from Syracuse's TRAC web API.

El pueblo unido jamás será vencido.

## structure

Backend: `/back` has a RESTful API in Python that uses an LSTM trained on ICE arrests to serve predicted future arrests by county.

Frontend: `/front` is used to display the predictions generated by the LSTM.

## installation

```
pip install -r requirements.txt
```
