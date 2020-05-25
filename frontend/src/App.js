import React from 'react';
import {
  BrowserRouter as Router,
  Switch,
  Route,
} from "react-router-dom";
import Header from './components/layout/Header';
import Landing from './components/Landing';
import Login from './components/Auth/Login';
import RegisterLender from './components/Auth/Register/RegisterLender';
import RegisterBorrower from './components/Auth/Register/RegisterBorrower';

export default function App() {
  return (
    <Router>
      <>
        <Header />
        <div className="container">
          <Switch>
            <Route exact path='/' component={Landing} />
          </Switch>
          <Switch>
            <Route exact path='/borrower' component={RegisterBorrower} />
          </Switch>
          <Switch>
            <Route exact path='/lender' component={RegisterLender} />
          </Switch>
          <Switch>
            <Route exact path='/login' component={Login} />
          </Switch>
        </div>
      </>
    </Router>
  )
}