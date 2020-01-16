import React from 'react';
import { useState, useEffect } from 'react';
import {withRouter} from 'react-router'
import logo from '../logo.svg';
import DatePicker from 'react-datepicker';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import Button from 'react-bootstrap/Button';
import Spinner from 'react-bootstrap/Spinner'


function Header({mindate, maxdate, fetchdata, settoday, location}){
  console.log(location);
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
        <Nav className='mr-auto navbar-right'>
          <Nav.Link href='/about'>
            about
          </Nav.Link>
          <Nav.Link href='/donate'>
            data by county
          </Nav.Link>
          <Nav.Link href='/safety'>
            safety
          </Nav.Link>
          <Nav.Link href='/donate'>
            donate
          </Nav.Link>
        </Nav>

        {location.pathname === '/' ?

          <DateForm
            maxdate={maxdate}
            mindate={mindate}
            fetchdata={fetchdata}
            settoday={settoday}/>

            :

            null}

      </Navbar.Collapse>
    </Navbar>
  );
}

function DateForm({mindate, maxdate, fetchdata, settoday}){

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
      <LoadingButton date={date} fetchdata={fetchdata} settoday={settoday}/>
    </div>
  );
}

function LoadingButton({fetchdata, date, settoday}) {

  const [isLoading, setLoading] = useState(false);

  useEffect(() => {
    if (isLoading) {
      fetchdata(date).then(r => {
        setLoading(false);
      });
      settoday(date)
    }
  }, [isLoading, date]);

  const handleClick = () => setLoading(true);

  return (
    <Button
      variant='outline-primary'
      className='mr-1 non-resizing'
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
