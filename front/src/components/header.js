import React from 'react';
import logo from '../logo.svg';
import './header.css';
import DatePicker from "react-datepicker";
import { useState } from 'react';
import Navbar from "react-bootstrap/Navbar";
import Nav from "react-bootstrap/Nav";
import Button from "react-bootstrap/Button";
import { Link } from "react-router-dom";

import Form from "react-bootstrap/Form";
import FormControl from "react-bootstrap/FormControl";

export default function Header(){
  return(
    <Navbar bg="light" expand="lg" sticky="top">
      <Navbar.Brand href="/">
        <img
          alt=""
          src={logo}
          width="30"
          height="30"
          className="d-inline-block align-top"
        />{' '}
        ai.melts.ice
      </Navbar.Brand>
      <Navbar.Toggle aria-controls="basic-navbar-nav" />
      <Navbar.Collapse id="basic-navbar-nav">
        <Nav className="mr-auto navbar-right">
          <Link to="/about">about</Link>
        </Nav>
        <DateForm/>
      </Navbar.Collapse>
    </Navbar>
  );
}

function DateForm(){
  const [date, setDate] = useState(new Date());
  return (
    <div>
      <DatePicker
        selected={date}
        onChange={date => setDate(date)}
        dateFormat="MM/yyyy"
        minDate={new Date(2015, 1)}
        maxDate ={new Date(2021, 12)}
        placeholderText="Select a month"
        showMonthYearPicker
      />
      {' '}
      <Button variant="outline-primary" className="mr-1">Search</Button>
    </div>
  );
}
