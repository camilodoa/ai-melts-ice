import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import * as serviceWorker from './serviceWorker';
import { BrowserRouter as Router} from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';


ReactDOM.render((
  <Router basename={process.env.PUBLIC_URL}>
    <App/>
  </Router>
), document.getElementById('root'));

serviceWorker.unregister();
