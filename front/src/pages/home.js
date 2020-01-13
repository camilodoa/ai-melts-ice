import React, { useState, useRef, useEffect } from 'react';
import logo from '../logo.svg';
import mapboxgl from 'mapbox-gl';
import token from '../tokens.js';

mapboxgl.accessToken = token.mapBoxToken;

export default function Home({data, today}) {

  const monthNames = ['January', 'February', 'March', 'April', 'May', 'June',
  'July', 'August', 'September', 'October', 'November', 'December'
  ];

  let mapContainer = useRef();
  const [lng, setlng] = useState(-96);
  const [lat, setlat] = useState(40);
  const [zoom, setzoom] = useState(4);

  function getMap() {
    const map = new mapboxgl.Map({
      container: mapContainer,
      style: 'mapbox://styles/mapbox/light-v10',
      center: [lng, lat],
      zoom: zoom
    });
    map.on('move', () => {
      setlng(map.getCenter().lng.toFixed(4));
      setlat(map.getCenter().lat.toFixed(4));
      setzoom(map.getZoom().toFixed(2));
    });
    map.on('load', () => {
      map.addSource('ai-melts-ice', {
        type: 'geojson',
        data: data,
      });
      console.log(data);
      map.addLayer({
        id: 'cirlces',
        type: 'circle',
        source: 'ai-melts-ice',
        filter: [">", 'arrests', 0],
        paint: {
          // Use step expressions (https://docs.mapbox.com/mapbox-gl-js/style-spec/#expressions-step)
          // with three steps to implement three types of circles:
          //   * Blue, 20px circles when point count is less than 100
          //   * Yellow, 30px circles when point count is between 100 and 500
          //   * Pink, 40px circles when point count is greater than or equal to 500
          'circle-color': [
            'step',
            ['get', 'arrests'],
            '#51bbd6',
            100,
            '#f1f075',
            500,
            '#f28cb1'
          ],
          'circle-radius': [
            'interpolate', ['linear'], ['zoom'],
            10, ['/',['get', 'arrests'], 10],
            13, ['/',['get', 'arrests'], 1]
          ],
          'circle-opacity': 0.8
        }
      });
      map.addLayer({
        id: 'count',
        type: 'symbol',
        source: 'ai-melts-ice',
        layout: {
          'text-field': ['get', 'arrests'],
          'text-font': ['DIN Offc Pro Medium', 'Arial Unicode MS Bold'],
          'text-size': ['interpolate', ['linear'], ['zoom'],
            10, ['/',['get', 'arrests'], 10],
            13, ['/',['get', 'arrests'], 1]
          ]
        }
      });

      // inspect a cluster on click
      map.on('click', 'arrests', function(e) {
        var features = map.queryRenderedFeatures(e.point, {
          layers: ['cirlces']
        });
        var circleId = features[0].properties.circles_id;
        map.getSource('ai-melts-ice').getClusterExpansionZoom(
          circleId,
          function(err, zoom) {
            if (err) return;

            map.easeTo({
              center: features[0].geometry.coordinates,
              zoom: zoom
            });
          }
        );
      });
    });
  };

  useEffect(() => {
    if (data !== null){
      getMap();
    }
  }, [data]);

  return (
    <div>

    { data === null ?
      <header className='body'>
        <img src={logo} className='logo' alt='logo'/>
        <p>
          ai.melts.ice
        </p>
      </header>

      :
      <div>
        <div className='sidebarStyle'>
          <div>{monthNames[today.getMonth()]}{' '}{today.getFullYear()}</div>
        </div>

        <div ref={el => mapContainer = el} className='mapContainer' />
      </div>
    }

    </div>
  );
}
