import React from "react";
import { Link } from "react-router-dom";

function AssetCard(props) {
  let title = props.asset.title.substring(0, 70);
  if (props.asset.title.length > 70) {
    title += "...";
  }

  return (
    <div className="column is-one-quarter-desktop is-half-tablet">
      <div className="card">
        <a href={"/asset/" + props.asset.media.mediaId}>
          <div className="card-image">
            <figure className="image is-4by3">
              <img
              src={"https://img.youtube.com/vi/" + props.asset.media.mediaId + "/0.jpg"} alt="Video Thumbnail" />
            </figure>
          </div>
        </a>

        <div className="card-content">
          <div className="media">
            <div className="media-content">
              <p className="title is-4">{title}</p>
              <p className="subtitle is-6">{props.asset.providerId}</p>
            </div>
          </div>

          <div className="content">
            Duration: {props.asset.media.durationInSeconds}s
          </div>
        </div>

        <footer className="card-footer">
          <Link className="card-footer-item" to={"/asset/" + props.asset.media.mediaId}>
            <span className="icon">
              <i className="fab fa-youtube"></i>
            </span>
            <span>
              Watch
            </span>
          </Link>

          <Link className="card-footer-item" to={{
            pathname: '/create-update',
            state: {
              asset: props.asset
            }
          }}>
            <span className="icon">
              <i className="fas fa-edit"></i>
            </span>
            <span>
              Edit
            </span>
          </Link>
        </footer>
      </div>
    </div>
  );
}

export default AssetCard;
