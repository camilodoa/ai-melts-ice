import React from 'react';
import Home from './pages/home';
import About from './pages/about';
import {Switch, Route} from 'react-router-dom';


export default function App({path}) {

  return (
    <div className='App'>
      <Switch>
        <Route exact path='/'>
          <Home/>
        </Route>
        <Route path='/about'>
          <About/>
        </Route>
      </Switch>
    </div>
  );

}
