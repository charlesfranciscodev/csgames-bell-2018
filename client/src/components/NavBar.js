import React, { Component } from 'react';

import { connect } from "react-redux";
import { userActions } from "../actions";

class NavBar extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isActive: false
    };
    this.toggleIsActive = this.toggleIsActive.bind(this);
    this.logoutButtonClick = this.logoutButtonClick.bind(this);
  }

  toggleIsActive() {
    this.setState(state => ({
      isActive: !state.isActive
    }));
  }

  logoutButtonClick() {
    const { dispatch } = this.props;
    dispatch(userActions.logout());
  }

  render() {
    const user = JSON.parse(localStorage.getItem("user"));
    let username = "";
    if (user) {
      username = user["hashedCredentials"].split(":")[0];
    }

    return (
      <nav className="navbar is-fixed-top" role="navigation" aria-label="main navigation">
        <div className="navbar-brand">
          <a className="navbar-item" href="https://bulma.io">
            <img src="https://bulma.io/images/bulma-logo.png" width="112" height="28" alt="Bulma Logo" />
          </a>
          <button className={"navbar-burger burger " + (this.state.isActive ? "is-active" : "")}
          aria-label="menu" aria-expanded="false" data-target="navbarBasicExample"
          onClick={this.toggleIsActive}>
            <span aria-hidden="true"></span>
            <span aria-hidden="true"></span>
            <span aria-hidden="true"></span>
          </button>
        </div>

        <div id="navbarBasicExample" className={"navbar-menu " + (this.state.isActive ? "is-active" : "")}>
          <div className="navbar-start">
            <a className="navbar-item" href="/">
              <span className="icon">
                <i className="fas fa-home"></i>
              </span>
              <span>
                Home
              </span>
            </a>

            <a className="navbar-item" href="/create">
              <span className="icon">
                <i className="far fa-plus-square"></i>
              </span>
              <span>
                Create Asset
              </span>
            </a>
          </div>

          { user ? (
          
          <div className="navbar-end">
            <div className="navbar-item">
              <div className="field">
                Welcome {username}!
              </div>
            </div>

            <div className="navbar-item">
              <div className="buttons">
                <button
                className="button is-light"
                onClick={this.logoutButtonClick}>
                  <span className="icon">
                    <i className="fas fa-sign-out-alt"></i>
                  </span>
                  <span>
                    Log out
                  </span>
                </button>
              </div>
            </div>
          </div>

          ) : (
          
          <div className="navbar-end">
            <div className="navbar-item">
              <div className="buttons">
                <a className="button is-primary" href="/register">
                  <span className="icon">
                    <i className="fas fa-user-plus"></i>
                  </span>
                  <span>
                    <strong>Register</strong>
                  </span>
                </a>

                <a className="button is-light" href="/login">
                  <span className="icon">
                    <i className="fas fa-sign-in-alt"></i>
                  </span>
                  <span>
                    Log in
                  </span>
                </a>
              </div>
            </div>
          </div>

          )}
        </div>
      </nav>
    );
  }
}

function mapStateToProps(state) {
  const { loggingOut } = state.authentication;
  return {
    loggingOut
  };
}

const connectedNavBar = connect(mapStateToProps)(NavBar);
export {connectedNavBar as NavBar};
