import React, { Component } from "react";
import NavBar from "./components/NavBar"
import Hero from "./components/HeroBanner"
import SearchAsset from "./components/SearchAsset"
import AssetGallery from "./components/AssetGallery"
import axios from 'axios';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      assets: []
    }
    this.search = this.search.bind(this);
  }

  componentDidMount() {
    this.search("");
  }

  search(query) {
    const url = `${process.env.REACT_APP_USERS_SERVICE_URL}/bell/search?query=${query}`;
    axios.get(url)
    .then(res => this.setState({assets: res.data}));
  }

  render() {
    return (
      <div>
        <NavBar />
        <Hero />
        <SearchAsset search={this.search} />
        <AssetGallery assets={this.state.assets} />
      </div>
    );
  }
}

export default App;
