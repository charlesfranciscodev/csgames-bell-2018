import React, { Component } from "react";

import "./Asset.css";

import { authHeader } from "../helpers";

class Asset extends Component {
  constructor(props) {
    super(props);

    this.state = {
      asset: undefined,
      error: undefined
    }
  }

  handleErrors(response) {
    if (!response.ok) {
        throw Error(response);
    }
    return response;
  }

  componentDidMount() {
    const { match: { params } } = this.props;
    const requestOptions = {
      method: "GET",
      headers: {
        ...authHeader()
      }
    }
    const url = `${process.env.REACT_APP_BELL_SERVICE_URL}/bell/asset/${params.mediaId}`;

    function handleResponse(response) {
      return response.json().then(data => {
        if (!response.ok) {
          return Promise.reject(data.message);
        }
        return data;
      });
    }

    fetch(url, requestOptions)
    .then(handleResponse)
    .then(data => this.setState({ asset: data }))
    .catch(error => this.setState({ error: error }));
  }

  render() {
    let url = "";
    if (this.state.asset) {
      url = `https://www.youtube.com/embed/${this.state.asset.media.mediaId}`;
    }

    return (
      <div>
      {
        this.state.asset ? (
          <section className="section">
            <div className="container">
              <div className="video-responsive">
                <iframe src={url}
                title={"iframe"}
                frameBorder="0"
                allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen />
              </div>
            </div>
          </section>
      ) : (
        <div className="container">
          <article className="message is-danger">
            <div className="message-body">
              {this.state.error}
            </div>
          </article>
        </div>
      )}
      </div>
    );
  }
}

export default Asset;
