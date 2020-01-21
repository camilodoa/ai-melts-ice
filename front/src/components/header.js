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
import FormControl from 'react-bootstrap/FormControl';


function Header( {
  mindate, maxdate, fetchdatedata, settoday, location,
  counties, fetchcountydata, sethere} ){
  return(
    <Navbar bg='light' expand='lg' sticky='top'>
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
          <Nav.Link href='/about'>
            About
          </Nav.Link>
          <Nav.Link href='/county'>
            Data by County
          </Nav.Link>
          <Nav.Link href='/safety'>
            Safety
          </Nav.Link>
          <Nav.Link href='/donate'>
            Donate
          </Nav.Link>
        </Nav>

        {location.pathname === '/' ?

          <DateForm
            maxdate={maxdate}
            mindate={mindate}
            fetchdatedata={fetchdatedata}
            settoday={settoday}/>

            :

            null}

        {location.pathname === '/county' ?

          <CountyForm
          counties={counties}
          fetchcountydata={fetchcountydata}
          sethere={sethere}/>

            :

            null}

      </Navbar.Collapse>
    </Navbar>
  );
}

function DateForm({mindate, maxdate, fetchdatedata, settoday}){

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
      <LoadingButton variable={date} fetch={fetchdatedata} setvariable={settoday}/>
    </div>
  );
}

function CountyForm({counties, fetchcountydata, sethere}){

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
        <FormControl
        className="mr-sm-2"
        sm="4"
        as="select"
        value={county}
        onChange={(e) => setcounty(e.target.value)}>
          {
            counties.counties.map((county, index) =>
              <option key={'county' + index}>{county}</option>
            )
          }
        </FormControl>
        {' '}
        <LoadingButton variable={county} fetch={fetchcountydata} setvariable={sethere}/>
      </Form>
    </div>
  );
}

function LoadingButton({fetch, variable, setvariable}) {

  const [isLoading, setLoading] = useState(false);

  useEffect(() => {
    if (isLoading) {
      fetch(variable).then(r => {
        setLoading(false);
      });
      setvariable(variable)
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
        'search'}
    </Button>
  );
}

export default withRouter(Header);
