import React from "react";
import { useState, useEffect, useRef } from 'react';
import api from '../rest';
import logo from '../logo.svg';
import Header from '../components/header';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import {
  HorizontalGridLines,
  VerticalGridLines,
  YAxis,
  XAxis,
  LineMarkSeries,
  XYPlot,
  Hint,
  ChartLabel
} from 'react-vis';


export default function County() {

  async function fetchcountydata(county) {
    let url = api.root + '/countydata/'+county.replace(' ', '%20');
    return await fetch(url).then(
      r => r.text()
    ).then(
      r => r = JSON.parse(r)
    ).then(r => {
      setcountydata(r);

      let localdata = r.data.map(datapoint => (
        {x : new Date(datapoint.date.split('-')[0], datapoint.date.split('-')[1]),
         y : datapoint.arrests}
      ));

      setdata(localdata);

      console.log(r);
    }).catch(
      err => console.log(err)
    );
  }

  // fetch counties from API
  async function fetchcounties() {
    let url = api.root + '/counties';
    return await fetch(url).then(
      r => r.text()
    ).then(
      r => r = JSON.parse(r)
    ).then(r => {
      setcounties(r);
    }).catch(
      err => console.log(err)
    );
  }

  // county data state
  const [countydata, setcountydata] = useState(null);

  // list of counties
  const [counties, setcounties] = useState({'counties' : ["Accomack County, VA"]});

  // current county
  const [here, sethere] = useState("Accomack County, VA");

  // displayed data
  const [data, setdata] = useState(null);

  const [value, setvalue] = useState(null);

  const size = useWindowSize();

  // component did mount
  useEffect(() => {
    // get county info
    fetchcounties();
    fetchcountydata(here);

  }, []);

  return (
    <div>
      <Header
        counties={counties}
        fetchcountydata={fetchcountydata}
        sethere={sethere}/>

      { data === null ?
        <header className='body'>
          <img src={logo} className='logo' alt='logo'/>
          <p>
            ai.melts.ice
          </p>
        </header>

        :

        <Container fluid>
          <Row className="align-items-md-center justify-content-md-center">
            <Col>
              <div className='sidebarStyle'>{here}</div>
              <div className='mt-5'>
                <XYPlot
                xType="time"
                height={size.height - size.height*.1 - 50}
                width={size.width  - 50}
                >
                  <HorizontalGridLines />
                  <VerticalGridLines />
                  <YAxis title="Arrests"/>
                  <XAxis/>
                  <LineMarkSeries
                  onValueMouseOver={(e) => setvalue(e)}
                  onValueMouseOut={(e) => setvalue(null)}
                  data={data}
                  color='#4285F4'/>
                  {value ? <Hint value={value} /> : null}
                </XYPlot>
              </div>
            </Col>
          </Row>
        </Container>


      }
    </div>
  );
}

// windowsize hook
function useWindowSize() {
  const isClient = typeof window === 'object';

  function getSize() {
    return {
      width: isClient ? window.innerWidth : undefined,
      height: isClient ? window.innerHeight : undefined
    };
  }

  const [windowSize, setWindowSize] = useState(getSize);

  useEffect(() => {
    if (!isClient) {
      return false;
    }

    function handleResize() {
      setWindowSize(getSize());
    }

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []); // Empty array ensures that effect is only run on mount and unmount

  return windowSize;
}
