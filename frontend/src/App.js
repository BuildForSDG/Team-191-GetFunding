import React from "react";
import {
  BrowserRouter as Router,
  Switch,
  Route,
} from "react-router-dom";
import Header from "./components/layout/Header/index";
import Landing from "./components/Landing/index";
import Login from "./components/Auth/Login/Login";
import Register from "./components/Auth/Register/Register";

export default function App() {
  return (
    <Router>
      <>
        <Header />
        <Switch>
          <Route exact path="/" component={Landing} />
        </Switch>
        <Switch>
          <Route path="/register" component={Register} />
        </Switch>
        <Switch>
          <Route path="/login" component={Login} />
        </Switch>
      </>
    </Router>
  );
}