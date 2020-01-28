import React from 'react';
import { useState, useEffect } from 'react';
import {withRouter} from 'react-router'
import logo from '../logo.svg';
import DatePicker from 'react-datepicker';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import Button from 'react-bootstrap/Button';
import Spinner from 'react-bootstrap/Spinner';
import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import Link from 'react-router-dom/Link';


function Header( {
  mindate, maxdate, fetchdatedata, settoday, location,
  counties, fetchcountydata, sethere} ){

    const [expanded, setexpanded] = useState(false);

  return(
    <Navbar bg='light' expand='lg' sticky='top' onToggle={setexpanded} expanded={expanded}>
      <Navbar.Brand href='/'>
        <img
          alt=''
          src={logo}
          width='30'
          height='30'
          className='d-inline-block align-top'
        />{' '}
        ai.melts.ice
      </Navbar.Brand>
      <Navbar.Toggle aria-controls='basic-navbar-nav' />
      <Navbar.Collapse id='basic-navbar-nav'>
        <Nav className='mr-auto'>
          <Nav.Link>
            <Link to='/'>
              Map
            </Link>
          </Nav.Link>
          <Nav.Link>
            <Link to='/county'>
              Arrests by County
            </Link>
          </Nav.Link>
          <Nav.Link>
            <Link to='/about'>
              About
            </Link>
          </Nav.Link>
          <Nav.Link>
            <Link to='/safety'>
              Safety
            </Link>
          </Nav.Link>
          <Nav.Link>
            <Link to='/donate'>
              Donate
            </Link>
          </Nav.Link>
        </Nav>

        {location.pathname === '/' ?
          <DateForm
            maxdate={maxdate}
            mindate={mindate}
            fetchdatedata={fetchdatedata}
            settoday={settoday}
            setexpanded={setexpanded}/>
            :
            null}

        {location.pathname === '/county' ?
          <CountyForm
          counties={counties}
          fetchcountydata={fetchcountydata}
          sethere={sethere}
          setexpanded={setexpanded}/>
            :
            null}

      </Navbar.Collapse>
    </Navbar>
  );
}

function DateForm({mindate, maxdate, fetchdatedata, settoday, setexpanded}){

  const [date, setdate] = useState(new Date());

  return (
    <div>
      <DatePicker
        selected={date}
        onChange={date => setdate(date)}
        dateFormat='MM/yyyy'
        minDate={mindate}
        maxDate ={maxdate}
        placeholderText='Select a month'
        showMonthYearPicker/>
      {' '}
      <LoadingButton
        variable={date}
        fetch={fetchdatedata}
        setvariable={settoday}
        setexpanded={setexpanded}/>
    </div>
  );
}

function CountyForm({counties, fetchcountydata, sethere, setexpanded}){

  const [county, setcounty] = useState(counties.counties[0]);

  return (
    <div>
      <Form
      inline
      onSubmit={(e) => {
        e.preventDefault();
        fetchcountydata(county);
        sethere(county);
      }}>
        <Form.Row>
          <Col xs>
            <Form.Control
            className="mr-sm-2"
            as="select"
            value={county}
            onChange={(e) => setcounty(e.target.value)}>
              {
                counties.counties.map((county, index) =>
                  <option key={'county' + index}>{county}</option>
                )
              }
            </Form.Control>
          </Col>
          <Col>
            <LoadingButton
              variable={county}
              fetch={fetchcountydata}
              setvariable={sethere}
              setexpanded={setexpanded}/>
          </Col>
        </Form.Row>
      </Form>
    </div>
  );
}

function LoadingButton({fetch, variable, setvariable, setexpanded}) {

  const [isLoading, setLoading] = useState(false);

  useEffect(() => {
    if (isLoading) {
      fetch(variable).then(r => {
        setLoading(false);
      });
      setvariable(variable);
      setexpanded(false);
    }
  }, [isLoading, variable]);

  const handleClick = () => setLoading(true);

  return (
    <Button
      variant='outline-primary'
      className='mr-1 non-resizing'
      type='submit'
      disabled={isLoading}
      onClick={!isLoading ? handleClick : null}
    >
      {isLoading ?
        <Spinner as='span' role='status' animation='border' variant='primary' size='sm' />
        :
        'Search'}
    </Button>
  );
}

export default withRouter(Header);
