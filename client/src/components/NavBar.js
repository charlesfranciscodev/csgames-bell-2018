import React, { Component } from 'react';

class NavBar extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isActive: false
    };
    this.toggleIsActive = this.toggleIsActive.bind(this);
  }

  toggleIsActive() {
    this.setState(state => ({
      isActive: !state.isActive
    }));
  }

  render() {
    return (
      <div className="container">
        <nav className="navbar" role="navigation" aria-label="main navigation">
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
                Home
              </a>
            </div>

            <div className="navbar-end">
              <div className="navbar-item">
                <div className="buttons">
                  <a className="button is-primary" href="/">
                    <strong>Sign up</strong>
                  </a>
                  <a className="button is-light" href="/">
                    Log in
                  </a>
                </div>
              </div>
            </div>
          </div>
        </nav>
      </div>
    );
  }
}

export default NavBar;
