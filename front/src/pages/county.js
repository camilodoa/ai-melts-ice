import React from "react";
import { useState, useEffect } from 'react';
import api from '../rest';
import logo from '../logo.svg';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';


export default function County() {
  async function fetchcountydata(county) {
    console.log(county);
    let url = api.root + '/countydata/'+county.replace(' ', '%20');
    return await fetch(url).then(
      r => r.text()
    ).then(
      r => r = JSON.parse(r)
    ).then(r => {
      setcountydata(r);
      console.log(r);
    }).catch(
      err => console.log(err)
    );
  }
  // county data state
  const [countydata, setcountydata] = useState(null);

  // fetch counties from API
  async function fetchcounties() {
    let url = api.root + '/counties';
    return await fetch(url).then(
      r => r.text()
    ).then(
      r => r = JSON.parse(r)
    ).then(r => {
      setcounties(r);
      console.log(r);
    }).catch(
      err => console.log(err)
    );
  }

  // date data state
  const [counties, setcounties] = useState(null);

  // component did mount
  useEffect(() => {
    fetchcounties();
  }, []);

  return (
    <div>
    { counties === null ?
      <header className='body'>
        <img src={logo} className='logo' alt='logo'/>
        <p>
          ai.melts.ice
        </p>
      </header>

      :
      <Container fluid>
        <Row>
          <Col className='county-form'>
            <Form onSubmit={(e) => {
              const form = e.target.value
              console.log(form);
              e.preventDefault();
              e.preventPropagation();
              fetchcountydata(e);
            }}>
              <Form.Group>
                <Form.Label>
                  <h4>
                    <p>
                      select a county
                    </p>
                  </h4>
                </Form.Label>
                <Form.Control as="select">
                  {
                    counties.data.map((county, index) =>
                      <option key={'county' + index}>{county}</option>
                    )
                  }
                </Form.Control>
              </Form.Group>
              <Button variant="primary" type='submit'>
                Submit
              </Button>
            </Form>
          </Col>
        </Row>

      </Container>
    }
    </div>
  );
}
