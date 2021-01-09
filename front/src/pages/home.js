import React, {useEffect, useRef, useState} from 'react';
import Header from './components/header';
import Popup from './components/popup';
import ReactDOM from 'react-dom';
import mapboxgl from 'mapbox-gl';
import token from '../tokens.js';
import api from '../rest';
import useWindowSize from '../window';
import logo from '../logo512.png';

mapboxgl.accessToken = token.mapBoxToken;

export default function Home() {
  // Utility definitions
  const monthNames = ['January', 'February', 'March', 'April', 'May', 'June',
  'July', 'August', 'September', 'October', 'November', 'December'];
  const size = useWindowSize();
  // Mapbox ref
  let mapContainer = useRef();
  // State
  const [lng] = useState(-96);
  const [lat] = useState(40);
  const [zoom] = useState(size.width < 550 ? 2 : 3.6);
  const[minDate, setMinDate] = useState(new Date(2015, 1));
  const [maxDate, setMaxDate] = useState(new Date(2020, 11));
  const [dateData, setDateData] = useState(null);
  const [today, setToday] = useState(new Date() <= maxDate ? new Date() : maxDate);
  console.log(today)
  // Lifecycle
  useEffect(() => {
    // Component did load
    fetchDates();
    fetchDateData(today);
  }, [today]);
  useEffect(() => {
    // Data loaded
    if (dateData !== null) {
      getMap();
    }
  }, [dateData]);
  // API calls
  async function fetchDates(){
    /*
    Fetch API date ranges
     */
    let url = api.root + '/dates';
    return await fetch(url).then(
        r => r.text()
    ).then(
        r => r = JSON.parse(r)
    ).then(r => {
      let minStr = r[0].split('-');
      let minYear = parseInt(minStr[0]);
      let minMonth = parseInt(minStr[1]);
      let maxStr = r[r.length - 1].split('-');
      let maxYear = parseInt(maxStr[0]);
      let maxMonth = parseInt(maxStr[1]) - 1;
      return [new Date(minYear, minMonth), new Date(maxYear, maxMonth)]
    }).then(date => {
      setMinDate(date[0]);
      setMaxDate(date[1]);
    }).catch(
        err => console.log(err)
    );
  }
  async function fetchCountyData (county) {
    /*
    Fetch county data given name
     */
    let url = api.root + '/countydata/' + county.replace(' ', '%20');
    return await fetch(url).then(
        r => r.text()
    ).then(
        r => r = JSON.parse(r)
    ).then(r => {
      return r.data.map(dataPoint => (
          {
            x: new Date(dataPoint.date.split('-')[0], dataPoint.date.split('-')[1]),
            y: dataPoint.arrests
          }
      ));
    }).catch(
        err => console.log(err)
    );
  }
  async function fetchDateData(date){
    /*
    Get monthly prediction from API
     */
    let url = api.root + '/predict/<month>/<year>';
    url = url.replace('<month>',
        date.getMonth() + 1).replace('<year>', date.getFullYear())
    return await fetch(url).then(
        r => r.text()
    ).then(
        r => r = JSON.parse(r)
    ).then(r => {
          setDateData(r);
        }
    ).catch(
        err => console.log(err)
    );
  }
  // Map
  function getMap() {
    /*
    Create a Mapbox map and attach it to mapContainer
     */
    const radiusSizes = size.width < 550 ? [ 30, 100, 40, 500, 50] : [ 30, 100, 40, 500, 60];
    const fontSizes = [ 20, 100, 30, 500, 40];
    const colors = ['#ffcc00', 100, '#ff9966', 500, '#cc3300'];
    const opacity = 0.7;
    const map = new mapboxgl.Map({
      container: mapContainer,
      style: 'mapbox://styles/camilodoa/ck9xqloge1g0f1ipj4y85tkzh',
      center: [lng, lat],
      zoom: zoom
    });
    map.on('load', () => {
      /*
      When the map loads, add all of its features
       */
      map.addSource('ai-melts-ice', {
        /*
        Load data into map
         */
        type: 'geojson',
        data: dateData['data'],
        cluster: true,
        clusterMaxZoom: 5,
        clusterRadius: 60,
        clusterProperties: {
          "arrests_sum": ["+", ['get', 'arrests']]
        }
      });
      map.addLayer({
        /*
        Add clustered circle symbol
         */
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
        /*
        Add clustered number of arrests
         */
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
        /*
        Add unclustered circle symbol
         */
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
        /*
        Add unclusted point number of arrests
         */
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
      map.on('click', 'cluster', function(e) {
        /*
       When the client clicks on an clustered point, zoom in
        */
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
      map.on('click', 'unclustered-point', function(e) {
        /*
        When the client clicks on an unclustered point, show popup
         */
        const coordinates = e.features[0].geometry.coordinates.slice();
        // Ensure that if the map is zoomed out such that multiple
        // copies of the feature are visible, the popup appears
        // over the copy being pointed to.
        while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
        coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
        }
        addPopup(e.features[0].properties.arrests, coordinates, e.features[0].properties.county)
      });
      async function addPopup(arrests, coordinates, county) {
        /*
        Adds popup to the map with customizable Popup component
         */
        let countyData = await fetchCountyData(county);
        const placeholder = document.createElement('popup');
        const predictionStart = dateData.predictionStart;
        ReactDOM.render(new Popup({
          arrests: arrests,
          county: county,
          countyData,
          predictionStart,
          today}), placeholder);
        new mapboxgl.Popup()
            .setDOMContent(placeholder)
            .setLngLat(coordinates)
            .addTo(map);
      }
      map.on('mouseenter', 'unclustered-point', function() {
        /*
        Change mouse appearance on clickable counties
         */
        map.getCanvas().style.cursor = 'pointer';
      });
      map.on('mouseleave', 'unclustered-point', function() {
        /*
       Change mouse appearance on clickable counties
        */
        map.getCanvas().style.cursor = '';
      });
      map.on('mouseenter', 'cluster', function() {
        /*
      Change mouse appearance on clickable counties
       */
        map.getCanvas().style.cursor = 'pointer';
      });

      map.on('mouseleave', 'cluster', function() {
        /*
      Change mouse appearance on clickable counties
       */
        map.getCanvas().style.cursor = '';
      });
    });
  }
  return (
    <div>
      <Header
        minDate={minDate}
        maxDate={maxDate}
        fetchDateData={fetchDateData}
        today={today}
        setToday={setToday}/>
        {dateData === null ?
          <h1 className='body header my-3 mt-5"'>
              <img src={logo} className='logo' alt='logo'/>
              <p className='header my-3'>
                AI Melts ICE
              </p>
              <p className="about-main">El pueblo unido jamás será vencido.</p>
          </h1>
          :
          <div className='map'>
            <div className='sidebarStyle'>
              <div>{dateData?
                      dateData['prediction'] ?
                        'Predicted ICE arrests for '
                        :
                        'ICE arrests from ' : null}
              {monthNames[today.getMonth()]}{' '}{today.getFullYear()}</div>
            </div>
            <div ref={el => mapContainer = el} className='mapContainer' />
          </div>
        }
    </div>
  );
}
