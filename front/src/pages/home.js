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
    map.on('load', () => {
      map.addSource('ai-melts-ice', {
        type: 'geojson',
        data: data,
        cluster: true,
        clusterMaxZoom: 10,
        clusterRadius: 50,
        clusterProperties: {
          "arrests_sum": ["+", ['get', 'arrests']]
        }
      });
      console.log(data);
      map.addLayer({
        id: 'cluster',
        type: 'circle',
        source: 'ai-melts-ice',
        filter: [">", 'arrests_sum', 0],
        paint: {
          // Use step expressions (https://docs.mapbox.com/mapbox-gl-js/style-spec/#expressions-step)
          // with three steps to implement three types of circles:
          //   * Blue, 20px circles when point count is less than 100
          //   * Yellow, 30px circles when point count is between 100 and 500
          //   * Pink, 40px circles when point count is greater than or equal to 500
          'circle-color': [
            'step',
            ['get', 'arrests_sum'],
            '#51bbd6',
            100,
            '#fce776',
            500,
            '#aa1929'
          ],
          'circle-radius': [
            'step',
            ['get', 'arrests_sum'],
            15,
            100,
            30,
            500,
            50
          ],
          'circle-opacity': 0.8
        }
      });
      map.addLayer({
        id: 'cluster-count',
        type: 'symbol',
        source: 'ai-melts-ice',
        filter: [">", 'arrests_sum', 0],
        layout: {
          'text-field': ['get', 'arrests_sum'],
          'text-font': ['DIN Offc Pro Medium', 'Arial Unicode MS Bold'],
          'text-size': [
            'step',
            ['get', 'arrests_sum'],
            10,
            100,
            20,
            500,
            40
          ]
        }
      });
      map.addLayer({
        id: 'unclustered-point',
        type: 'circle',
        source: 'ai-melts-ice',
        filter: ["all", ['!has', 'point_count'], [">", 'arrests', 0]],
        paint: {
          'circle-color': [
            'step',
            ['get', 'arrests'],
            '#51bbd6',
            100,
            '#fce776',
            500,
            '#aa1929'
          ],
          'circle-radius': [
            'step',
            ['get', 'arrests'],
            15,
            100,
            30,
            500,
            50
          ],
          'circle-opacity': 0.8
        }
      });
      map.addLayer({
        id: 'unclustered-count',
        type: 'symbol',
        source: 'ai-melts-ice',
        filter: ["all", ['!has', 'point_count'], [">", 'arrests', 0]],
        layout: {
          'text-field': ['get', 'arrests'],
          'text-font': ['DIN Offc Pro Medium', 'Arial Unicode MS Bold'],
          'text-size': [
            'step',
            ['get', 'arrests'],
            10,
            100,
            20,
            500,
            40
          ]
        }
      });

      // inspect a cluster on click
      map.on('click', 'cluster', function(e) {
        var features = map.queryRenderedFeatures(e.point, {
          layers: ['cluster']
        });
        var clusterId = features[0].properties.cluster_id;
        map.getSource('ai-melts-ice').getClusterExpansionZoom(
          clusterId,
          function(err, zoom) {
            if (err) return;

            map.easeTo({
              center: features[0].geometry.coordinates,
              zoom: zoom
            });
          }
        );
      });

      map.on('mouseenter', 'cluster', function() {
        map.getCanvas().style.cursor = 'pointer';
      });

      map.on('mouseleave', 'cluster', function() {
        map.getCanvas().style.cursor = '';
      });

      map.on('click', 'unclustered-point', function(e) {
        var coordinates = e.features[0].geometry.coordinates.slice();
        var description = '<div class="my-2"><strong>' + e.features[0].properties.county +
            '</strong><p>' + e.features[0].properties.arrests + ' arrests</p></div>';

        // Ensure that if the map is zoomed out such that multiple
        // copies of the feature are visible, the popup appears
        // over the copy being pointed to.
        while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
        coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
        }

        new mapboxgl.Popup()
          .setLngLat(coordinates)
          .setHTML(description)
          .addTo(map);
      });

      map.on('mouseenter', 'unclustered-point', function() {
        map.getCanvas().style.cursor = 'pointer';
      });

      map.on('mouseleave', 'unclustered-point', function() {
        map.getCanvas().style.cursor = '';
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
