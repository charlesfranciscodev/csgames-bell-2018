import React, { Component } from "react";
import AssetCard from "./AssetCard"
import PropTypes from "prop-types";

class AssetGallery extends Component {
  render() {
    return (
      <section className="section">
        <div className="container">
          <div className="columns is-multiline">
            {this.props.assets.map(
              asset => (
                <AssetCard key={asset.media.mediaId} asset={asset} />
              )
            )}
          </div>
        </div>
      </section>
    );
  }
}

AssetGallery.propTypes = {
  assets: PropTypes.array.isRequired
}

export default AssetGallery;
