import React from 'react';
import {useState, useEffect} from 'react';
import {withRouter} from 'react-router'
import DatePicker from 'react-datepicker';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import Button from 'react-bootstrap/Button';
import Spinner from 'react-bootstrap/Spinner';
import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import {FaSistrix} from 'react-icons/fa';
import logo from '../images/logo512.png';


function Header({
                    mindate, maxdate, fetchdatedata, settoday, location,
                    counties, fetchcountydata, sethere
                }) {
    return (
        <Navbar bg='light' expand='lg' sticky='top'>
            <Navbar.Brand href='/'>
                <img src={logo} className="d-inline-block align-top" height="30" width="30" alt="logo"/>
                {' '}
                AI Melts ICE
            </Navbar.Brand>
            <Nav className='ml-sm-auto ml-xs-0 my-2'>
              {location.pathname === '/' ?
                  <DateForm
                      maxdate={maxdate}
                      mindate={mindate}
                      fetchdatedata={fetchdatedata}
                      settoday={settoday}/>
                  :
                  null}
            </Nav>
            <Nav className='ml-sm-auto ml-xs-0'>
                <Nav.Link href='/about'>
                    About
                </Nav.Link>
            </Nav>
        </Navbar>
    );
}

function DateForm({mindate, maxdate, fetchdatedata, settoday}) {

    const [date, setdate] = useState(new Date());

    return (
        <div>

            <DatePicker
                selected={date}
                onChange={date => {
                    setdate(date);
                    fetchdatedata(date);
                    settoday(date);
                }}
                dateFormat='MMMM yyyy'
                minDate={mindate}
                maxDate={maxdate}
                placeholderText='Select a month'
                showMonthYearPicker/>

            <FaSistrix className={'mx-2'} size={'1em'}/>

        </div>
    );
}


export default withRouter(Header);
