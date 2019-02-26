import React from "react";

function AssetCard(props) {
  return (
    <div className="column is-one-quarter-desktop is-half-tablet">
      <div className="card">
        <div className="card-image">
          <figure className="image is-4by3">
            <img
            src={"https://img.youtube.com/vi/" + props.asset.media.mediaId + "/0.jpg"} alt="Video Thumbnail" />
          </figure>
        </div>

        <div className="card-content">
          <div className="media">
            <div className="media-content">
              <p className="title is-4">{props.asset.title}</p>
              <p className="subtitle is-6">{props.asset.providerId}</p>
            </div>
          </div>

          <div className="content">
            Duration: {props.asset.media.durationInSeconds}s
          </div>
        </div>

        <footer className="card-footer">
          <a href="/" className="card-footer-item">
            <span class="icon">
              <i class="fab fa-youtube"></i>
            </span>
            <span>
              Watch
            </span>
          </a>
          <a href="/" className="card-footer-item">
            <span class="icon">
              <i class="fas fa-edit"></i>
            </span>
            <span>
              Edit
            </span>
          </a>
        </footer>
      </div>
    </div>
  );
}

export default AssetCard;
