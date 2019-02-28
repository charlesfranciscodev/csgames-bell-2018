import React, { Component } from "react";
import HeroBanner from "./HeroBanner";
import SearchAsset from "./SearchAsset";
import AssetGallery from "./AssetGallery";

class HomePage extends Component {
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
    const url = `${process.env.REACT_APP_BELL_SERVICE_URL}/bell/search?query=${query}`;
    fetch(url)
    .then(response => response.json())
    .then(data => this.setState({assets: data}));
  }

  render() {
    return (
      <div>
        <HeroBanner />
        <SearchAsset search={this.search} />
        <AssetGallery assets={this.state.assets} />
      </div>
    );
  }
}

export default HomePage;
