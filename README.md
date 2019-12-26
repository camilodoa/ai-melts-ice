# ai-melts-ice

repo for AI - Melts - ICE
made by @camilodoa

Backend: `/back/` has a RESTful API in Python that queries the U.S. FEDERAL API
for data on ICE raids (location, time, number taken). Uses that data using an
HMM / BDN to use predict future raids.

Frontend: `/front/`, made in React, is used to display the predictions for X
days ahead.

## installation

```
pip install -r requirements.txt
```
