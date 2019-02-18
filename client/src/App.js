import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import axios from 'axios';

class App extends Component {
  constructor() {
    super();
    this.state = {
      ping: ""
    };
  };

  componentDidMount() {
    this.getPing();
  }

  getPing() {
    axios.get(`${process.env.REACT_APP_USERS_SERVICE_URL}/app/ping`)
    .then((res) => {
      this.setState({
        ping: res.data
      });
      console.log(res.data);
    })
    .catch((err) => { console.log(err); });
  }

  render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <p>
            Edit <code>src/App.js</code> and save to reload.
          </p>
          <a
            className="App-link"
            href="https://reactjs.org"
            target="_blank"
            rel="noopener noreferrer"
          >
            Learn React
          </a>

          <p>
            AJAX call: {this.state.ping.message}
          </p>
          
        </header>
      </div>
    );
  }
}

export default App;
