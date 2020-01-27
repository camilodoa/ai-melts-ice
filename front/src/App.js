import React from 'react';
import Footer from './components/footer';
import Home from './pages/home';
import About from './pages/about';
import Safety from './pages/safety';
import Donate from './pages/donate';
import County from './pages/county';
import {Switch, Route} from 'react-router-dom';


export default function App({path}) {

  return (
    <div>

      <div className='App'>
        <Switch>
          <Route exact path='/'>
            <Home/>
          </Route>
          <Route path='/about'>
            <About/>
          </Route>
          <Route path='/safety'>
            <Safety/>
          </Route>
          <Route path='/donate'>
            <Donate/>
          </Route>
          <Route path='/county'>
            <County/>
          </Route>
        </Switch>
      </div>

      <Footer/>
    </div>
  );

}
