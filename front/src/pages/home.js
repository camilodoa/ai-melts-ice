import React, { useState, useRef, useEffect } from 'react';
import Header from '../components/header';
import Spinner from 'react-bootstrap/Spinner';
import logo from '../images/logo512.png';
import mapboxgl from 'mapbox-gl';
import token from '../tokens.js';
import api from '../rest';
import useWindowSize from '../hooks/window';


mapboxgl.accessToken = token.mapBoxToken;

export default function Home() {

  // map render functions + state ==============================================
  const monthNames = ['January', 'February', 'March', 'April', 'May', 'June',
  'July', 'August', 'September', 'October', 'November', 'December'
  ];

  const size = useWindowSize();

  let mapContainer = useRef();
  const [lng] = useState(-96);
  const [lat] = useState(40);
  const [zoom] = useState(size.width < 550 ? 2 : 3);

  function getMap() {
    const radiusSizes = [ 30, 100, 40, 500, 60];
    const fontSizes = [ 20, 100, 30, 500, 40];
    const colors = ['#ffcc00', 100, '#ff9966', 500, '#cc3300'];
    const opacity = 0.9;
    const map = new mapboxgl.Map({
      container: mapContainer,
      style: 'mapbox://styles/camilodoa/ck9xqloge1g0f1ipj4y85tkzh',
      center: [lng, lat],
      zoom: zoom
    });
    map.on('load', () => {
      map.addSource('ai-melts-ice', {
        type: 'geojson',
        data: datedata,
        cluster: true,
        clusterMaxZoom: 5,
        clusterRadius: 60,
        clusterProperties: {
          "arrests_sum": ["+", ['get', 'arrests']]
        }
      });
      map.addLayer({
        id: 'cluster',
        type: 'circle',
        source: 'ai-melts-ice',
        filter: [">", 'arrests_sum', 0],
        paint: {
          'circle-color': [
            'step',
            ['get', 'arrests_sum'],
            colors[0],
            colors[1],
            colors[2],
            colors[3],
            colors[4]
          ],
          'circle-radius': [
            'step',
            ['get', 'arrests_sum'],
            radiusSizes[0],
            radiusSizes[1],
            radiusSizes[2],
            radiusSizes[3],
            radiusSizes[4]
          ],
          'circle-opacity': opacity
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
            fontSizes[0],
            fontSizes[1],
            fontSizes[2],
            fontSizes[3],
            fontSizes[4]
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
            colors[0],
            colors[1],
            colors[2],
            colors[3],
            colors[4]
          ],
          'circle-radius': [
            'step',
            ['get', 'arrests'],
            radiusSizes[0],
            radiusSizes[1],
            radiusSizes[2],
            radiusSizes[3],
            radiusSizes[4]
          ],
          'circle-opacity': opacity
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
            fontSizes[0],
            fontSizes[1],
            fontSizes[2],
            fontSizes[3],
            fontSizes[4]
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
            '<div class="about-main py-2" style="line-height: 1.5;"><strong class="my-3">' +
              e.features[0].properties.county +
            '</strong><p class="my-3">' +
            e.features[0].properties.arrests + ' arrest</p></div>'
            :
            '<div class="about-main py-2" style="line-height: 1.5;"><strong class="my-3">' +
            e.features[0].properties.county +
            '</strong><p class="my-3">' +
            e.features[0].properties.arrests + ' arrests</p></div>';

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
        {
          datedata === null ?
          <header className='body'>
            <p>
              ai melts ice
            </p>
            <Spinner animation="grow" variant="dark" role="status"/>
          </header>
          :
          <div className='map'>
            <div className='sidebarStyle'>
              <div>{monthNames[today.getMonth()]}{' '}{today.getFullYear()}</div>
            </div>
            <div ref={el => mapContainer = el} className='mapContainer' />
          </div>
        }
    </div>
  );
}
