import React from 'react';
import logo from './logo.svg';
import './App.css';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";
import Navbar from "react-bootstrap/Navbar";
import Nav from "react-bootstrap/Nav";
import NavDropdown from "react-bootstrap/NavDropdown";
import Form from "react-bootstrap/Form";
import FormControl from "react-bootstrap/FormControl";
import Button from "react-bootstrap/Button";
import { useState } from 'react';
import Footer from "./components/footer";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";



function App() {
  return (
    <div>
      <div className="App">
        <Navbar bg="light" expand="lg">
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
              <Nav.Link href="/about">About</Nav.Link>
            </Nav>
            <DateForm/>
          </Navbar.Collapse>
        </Navbar>
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo"/>
          <p>
            ai.melts.ice
          </p>
        </header>
      </div>
      <Footer/>
    </div>
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
      <Button variant="outline-success">Search</Button>
    </div>
  );
}

export default App;
