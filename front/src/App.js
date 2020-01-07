import React from 'react';
import './App.css';
import Footer from './components/footer';
import Header from './components/header';

import Home from './pages/home';
import About from './pages/about';
import {
  Switch,
  Route
} from 'react-router-dom';


export default function App() {
  return (
    <div>
      <div className='App'>
        <Header/>

        <Switch>
          <Route exact path='/'>
            <Home/>
          </Route>
          <Route path='/about'>
            <About/>
          </Route>
        </Switch>
      </div>

      <Footer/>
    </div>
  );
}
