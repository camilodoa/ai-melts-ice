import React from 'react';
import { useState, useEffect } from 'react';
import logo from '../logo.svg';
import './header.css';
import DatePicker from 'react-datepicker';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import Button from 'react-bootstrap/Button';
import Spinner from 'react-bootstrap/Spinner'
import { Link } from 'react-router-dom';


export default function Header(){

  async function fetchdates(){
    let url = 'http://0.0.0.0:8080/start';
    return await fetch(url).then(
      r => r.text()
    ).then(
      r => r = JSON.parse(r)
    ).catch(
      err => console.log(err)
    );
  }

  const[mindate, setmindate] = useState(new Date(2015, 1));
  const [maxdate, setmaxdate] = useState(new Date(2021, 12));

  useEffect(() => {
    fetchdates().then(r => {
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
    });
  }, []);

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
          <Link to='/about'>about</Link>
        </Nav>
        <DateForm maxdate={maxdate} mindate={mindate}/>
      </Navbar.Collapse>
    </Navbar>
  );
}

function DateForm(props){

  const [date, setDate] = useState(new Date());

  return (
    <div>
      <DatePicker
        selected={date}
        onChange={date => setDate(date)}
        dateFormat='MM/yyyy'
        minDate={props.mindate}
        maxDate ={props.maxdate}
        placeholderText='Select a month'
        showMonthYearPicker
      />
      {' '}
      <LoadingButton date={date}/>
    </div>
  );
}

function LoadingButton(props) {

  async function fetchdata(date){
    let url = 'http://0.0.0.0:8080/predict/<month>/<year>';
    url = url.replace('<month>', date.getMonth() + 1).replace('<year>', date.getFullYear())
    return await fetch(url).then(
      r => r.text()
    ).then(
      r => r = JSON.parse(r)
    ).catch(
      err => console.log(err)
    );
  }

  const [isLoading, setLoading] = useState(false);

  useEffect(() => {
    if (isLoading) {
      fetchdata(props.date).then(r => {
        console.log(r);
        setLoading(false);
      });
    }
  }, [isLoading, props.date]);

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
