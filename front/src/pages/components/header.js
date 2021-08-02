import React from 'react';
import {withRouter} from 'react-router'
import DatePicker from 'react-datepicker';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import logo from '../../logo512.png';

function Header({minDate, maxDate, fetchDateData, today, setToday, location}) {
    return (
        <Navbar bg='light' expand='lg' sticky='top'>
            <Navbar.Brand href='/'>
                <img src={logo} className="d-inline-block align-top" height="30" width="30" alt="logo"/>
                {' '}
                AI Melts ICE
            </Navbar.Brand>
            <Nav className='ml-sm-auto ml-xs-0 my-2' xs={{ order: 12 }}>
                {location.pathname === '/' &&
                        <DatePicker
                            selected={today}
                            onChange={date => {
                                fetchDateData(date);
                                setToday(date);
                            }}
                            dateFormat='MMMM yyyy'
                            minDate={minDate}
                            maxDate={maxDate}
                            placeholderText='Select a month'
                            showMonthYearPicker/>

                    }
            </Nav>
            <Nav className='ml-sm-auto ml-xs-0' xs={{ order: 1 }}>
                <Nav.Link href='/about'>
                    About
                </Nav.Link>
            </Nav>
        </Navbar>
    );
}
export default withRouter(Header);
