import React from 'react';
import { useState, useEffect } from 'react';
import Footer from './components/footer';
import Header from './components/header';
import Home from './pages/home';
import About from './pages/about';
import {Switch, Route} from 'react-router-dom';


export default function App() {
  // fetch date range from API
  async function fetchdates(){
    let url = 'http://0.0.0.0:8080/start';
    return await fetch(url).then(
      r => r.text()
    ).then(
      r => r = JSON.parse(r)
    ).then(r => {
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
    }).catch(
      err => console.log(err)
    );
  }
  // min and max state
  const[mindate, setmindate] = useState(new Date(2015, 1));
  const [maxdate, setmaxdate] = useState(new Date(2021, 12));

  // fetch date data from API
  async function fetchdata(date){
    let url = 'http://0.0.0.0:8080/predict/<month>/<year>';
    url = url.replace('<month>', date.getMonth() + 1).replace('<year>', date.getFullYear())
    return await fetch(url).then(
      r => r.text()
    ).then(
      r => r = JSON.parse(r)
    ).then(r => {
        setdata(r);
      }
    ).catch(
      err => console.log(err)
    );
  }
  // date data state
  const [data, setdata] = useState(null);

  // current date that data is being displayed for
  const [today, settoday] = useState(new Date() <= maxdate ? new Date() : maxdate);

  // component did mount
  useEffect(() => {
    fetchdates();

    fetchdata(today);
  }, []);

  return (
    <div>
      <div className='App'>
        <Header
          mindate={mindate}
          maxdate={maxdate}
          fetchdata={fetchdata}
          settoday={settoday}/>

        <Switch>
          <Route exact path='/'>
            <Home data={data} today={today}/>
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
