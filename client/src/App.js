import React, { Component } from "react";
import NavBar from "./components/NavBar"
import Hero from "./components/HeroBanner"
import AssetGallery from "./components/AssetGallery"
import axios from 'axios';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      assets: []
    }
  }

  componentDidMount() {
    axios.get(`${process.env.REACT_APP_USERS_SERVICE_URL}/bell/search?query=`)
    .then(res => this.setState({assets: res.data}));
  }

  render() {
    return (
      <div>
        <NavBar />
        <Hero />
        <AssetGallery assets={this.state.assets} />
      </div>
    );
  }
}

export default App;
