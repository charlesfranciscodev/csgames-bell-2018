import React, { Component } from "react";

import "./Asset.css";

import { authHeader } from "../helpers";

class Asset extends Component {
  constructor(props) {
    super(props);

    this.state = {
      asset: undefined,
      error: undefined,
      filter: ""
    }

    this.onSelectChange = this.onSelectChange.bind(this);
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

  onSelectChange(e) {
    let value = e.target.value;
    this.setState({
      filter: value
    });
  }

  render() {
    let url = "";
    if (this.state.asset) {
      url = `https://www.youtube.com/embed/${this.state.asset.media.mediaId}`;
    }

    let videoStyle = {
      filter: "url(#" + this.state.filter + ")"
    };

    return (
      <div>
      { this.state.asset ? (
        <div className="container">
          <div className="video-responsive" style={videoStyle}>
            <iframe src={url}
            title={"iframe"}
            frameBorder="0"
            allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"
            />
          </div>

          <div id="selectFilter" className="field">
            <div className="control">
              <div className="select">
                <select
                name="filter"
                onChange={this.onSelectChange}>
                  <option value="">none</option>
                  <option value="blur">blur</option>
                  <option value="inverse">inverse</option>
                  <option value="convolve">convolve</option>
                  <option value="convoblur">convoblur</option>
                  <option value="blackandwhite">black and white</option>
                  <option value="noir">noir</option>
                  <option value="displacement">displacement</option>
                </select>
              </div>
            </div>
          </div>

          <svg id="image" version="1.1" xmlns="http://www.w3.org/2000/svg">
            <defs>
              <filter id="blur">
                <feGaussianBlur stdDeviation="10,3" result="outBlur"/>
              </filter>

              <filter id="inverse">
                <feComponentTransfer>
                  <feFuncR type="table" tableValues="1 0"/>
                  <feFuncG type="table" tableValues="1 0"/>
                  <feFuncB type="table" tableValues="1 0"/>
                </feComponentTransfer>
              </filter>

              <filter id="convolve">
                <feConvolveMatrix order="3" kernelMatrix="1 -1  1 -1 -0.01 -1 1 -1 1" edgeMode="duplicate" result="convo"/>
              </filter>

              <filter id="convoblur">
                <feGaussianBlur in="SourceGraphic" stdDeviation="6" result="blur"/>
                <feConvolveMatrix order="3" kernelMatrix="1 -1  1 -1 -0.01 -1 1 -1 1" edgeMode="none" result="convo"/>
                <feMerge>
                  <feMergeNode in="blur"/>
                  <feMergeNode in="convo"/>
                </feMerge>
              </filter>

              <filter id="blackandwhite">
                <feColorMatrix values="0.3333 0.3333 0.3333 0 0
                  0.3333 0.3333 0.3333 0 0
                  0.3333 0.3333 0.3333 0 0
                  0      0      0      1 0"/>
              </filter>

              <filter id="noir">
                <feGaussianBlur stdDeviation="1.5" />
                <feComponentTransfer>
                  <feFuncR type="discrete" tableValues="0 .5 1 1"/>
                  <feFuncG type="discrete" tableValues="0 .5 1"/>
                  <feFuncB type="discrete" tableValues="0"/>
                </feComponentTransfer>
              </filter>

              <filter id="displacement" x="0%" y="0%" height="100%" width="100%">
                <feDisplacementMap scale="100" in2="SourceGraphic" xChannelSelector="G"/>
              </filter>
            </defs>
          </svg>
        </div>
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
