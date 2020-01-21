import React, { useState, useRef, useEffect } from 'react';
import Header from '../components/header';
import logo from '../logo.svg';
import mapboxgl from 'mapbox-gl';
import token from '../tokens.js';
import api from '../rest';


mapboxgl.accessToken = token.mapBoxToken;

export default function Home() {

  // map render functions + state ==============================================
  const monthNames = ['January', 'February', 'March', 'April', 'May', 'June',
  'July', 'August', 'September', 'October', 'November', 'December'
  ];

  let mapContainer = useRef();
  const [lng] = useState(-96);
  const [lat] = useState(40);
  const [zoom] = useState(4);

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
        data: datedata,
        cluster: true,
        clusterMaxZoom: 4,
        clusterRadius: 50,
        clusterProperties: {
          "arrests_sum": ["+", ['get', 'arrests']]
        }
      });
      console.log(datedata);
      map.addLayer({
        id: 'cluster',
        type: 'circle',
        source: 'ai-melts-ice',
        filter: [">", 'arrests_sum', 0],
        paint: {
          'circle-color': [
            'step',
            ['get', 'arrests_sum'],
            '#fce776',
            100,
            '#ec5300',
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
            '#fce776',
            100,
            '#ec5300',
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
        var description = e.features[0].properties.arrests === 1 ?
            '<div class="my-2"><strong>' + e.features[0].properties.county +
            '</strong><p>' + e.features[0].properties.arrests + ' arrest</p></div>'
            :
            '<div class="my-2"><strong>' + e.features[0].properties.county +
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


  // date data fetch functions + state =========================================

  // fetch date range from API
  async function fetchdates(){
    let url = api.root + '/dates';
    return await fetch(url).then(
      r => r.text()
    ).then(
      r => r = JSON.parse(r)
    ).then(r => {
      let minstr = r[0].split('-');
      let minyear = parseInt(minstr[0]);
      let minmonth = parseInt(minstr[1]);

      let maxstr = r[r.length - 1].split('-');
      let maxyear = parseInt(maxstr[0]);
      let maxmonth = parseInt(maxstr[1]);

      return [new Date(minyear, minmonth), new Date(maxyear, maxmonth)]
    }).then(date => {
      setmindate(date[0]);
      setmaxdate(date[1]);
    }).catch(
      err => console.log(err)
    );
  }

  // fetch date data from API
  async function fetchdatedata(date){
    let url = api.root + '/predict/<month>/<year>';
    url = url.replace('<month>', date.getMonth() + 1).replace('<year>', date.getFullYear())
    return await fetch(url).then(
      r => r.text()
    ).then(
      r => r = JSON.parse(r)
    ).then(r => {
        setdatedata(r);
      }
    ).catch(
      err => console.log(err)
    );
  }

  // min and max state
  const[mindate, setmindate] = useState(new Date(2015, 1));
  const [maxdate, setmaxdate] = useState(new Date(2021, 12));
  // date data state
  const [datedata, setdatedata] = useState(null);
  // current date that data is being displayed for
  const [today, settoday] = useState(new Date() <= maxdate ? new Date() : maxdate);


  // lifecycle functions =======================================================

  // component did mount
  useEffect(() => {
    // get date and US info
    fetchdates();
    fetchdatedata(today);

  }, []);

  // updates on change of date data
  useEffect(() => {
    if (datedata !== null) {
      getMap();
    }
  }, [datedata]);

  return (
    <div>

      <Header
        mindate={mindate}
        maxdate={maxdate}
        fetchdatedata={fetchdatedata}
        settoday={settoday}/>

      <div>
        { datedata === null ?
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

    </div>
  );
}
