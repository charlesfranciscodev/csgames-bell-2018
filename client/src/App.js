import React, { Component } from "react";
import { NavBar } from "./components/NavBar";
import HomePage from "./components/HomePage";
import { LoginPage } from "./components/LoginPage";
import { RegisterPage } from "./components/RegisterPage"
import Asset from "./components/Asset";
import CreateUpdateAsset from "./components/CreateUpdateAsset";

import { Router, Route } from "react-router-dom";
import { connect } from "react-redux";
import { history } from "./helpers";
import { alertActions } from './actions';

class App extends Component {
  constructor(props) {
    super(props);

    const { dispatch } = this.props;
    history.listen((location, action) => {
        // clear alert on location change
        dispatch(alertActions.clear());
    });
    this.alertButtonClick = this.alertButtonClick.bind(this);
  }

  alertButtonClick() {
    const { dispatch } = this.props;
    dispatch(alertActions.clear());
  }

  render() {
    const { alert } = this.props;
    return (
      <div>
        <Router history={history}>
          <div>
            <NavBar />

            {alert.message &&
              <div className="container">
                <div
                className={`notification + ${alert.type}`}>
                  <button className="delete" onClick={this.alertButtonClick} />
                  { alert.message }
                </div>
              </div>
            }

            <Route exact path="/" component={HomePage} />
            <Route path="/login" component={LoginPage} />
            <Route path="/register" component={RegisterPage} />
            <Route path="/asset/:mediaId" component={Asset} />
            <Route path="/create-update" component={CreateUpdateAsset} />
          </div>
        </Router>
      </div>
    );
  }
}

function mapStateToProps(state) {
  const { alert } = state;
  return {
    alert
  };
}

const connectedApp = connect(mapStateToProps)(App);
export { connectedApp as App };
