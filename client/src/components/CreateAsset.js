import React, { Component } from "react";

import {parse, toSeconds} from 'iso8601-duration';

import { authHeader } from "../helpers";

import { history } from "../helpers";

class CreateAsset extends Component {
  constructor(props) {
    super(props);

    this.state = {
      allProviders: [], // API
      allProfiles: [], // API
      providerId: "",
      title: "", // YouTube API/form field
      licensingWindowStart: "", // form field
      licensingWindowEnd: "", // form field
      profiles: [], // form field
      mediaId: "", // form field
      duration: "", // YouTube API
      submitted: false,
      error: ""
    }

    this.onChange = this.onChange.bind(this);
    this.onMediaIdChange = this.onMediaIdChange.bind(this);
    this.onSelectChange = this.onSelectChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  componentDidMount() {
    const urlProfiles = `${process.env.REACT_APP_BELL_SERVICE_URL}/bell/profiles`;
    fetch(urlProfiles)
    .then(response => response.json())
    .then(data => this.setState({allProfiles: data}));

    const urlProviders = `${process.env.REACT_APP_BELL_SERVICE_URL}/bell/providers`;
    fetch(urlProviders)
    .then(response => response.json())
    .then(data => this.setState({
      providerId: data[0].providerId,
      allProviders: data
    }));
  }

  onMediaIdChange(e) {
    const value = e.target.value;
    this.setState({
      mediaId: value
    })
    const url = `${process.env.REACT_APP_YOUTUBE_DATA_API_URL}/videos?id=${value}&part=snippet,contentDetails&key=${process.env.REACT_APP_YOUTUBE_DATA_API_KEY}`;
    fetch(url)
    .then(response => response.json())
    .then(data =>
      this.setState({
        title: data.items[0].snippet.title,
        duration: data.items[0].contentDetails.duration
      })
    );
  }

  onChange(e) {
    this.setState({
      [e.target.name]: e.target.value
    });
  }

  onSelectChange(e) {
    let options = e.target.options;
    let array = [];
    for (let i = 0; i < options.length; i++) {
      if (options[i].selected) {
        array.push(options[i].value);
      }
    }
    this.setState({
      profiles: array
    });
  }

  handleSubmit(e) {
    e.preventDefault();
    let durationInSeconds = 0;
    if (this.state.duration) {
      durationInSeconds = toSeconds(parse(this.state.duration));
    }
    this.setState({ submitted: true });
    this.setState({ error: "" });
    const asset = {
      providerId: this.state.providerId,
      title: this.state.title,
      licensingWindow: {
        start: this.state.licensingWindowStart,
        end: this.state.licensingWindowEnd
      },
      profileIds: this.state.profiles,
      media: {
        mediaId: this.state.mediaId,
        durationInSeconds: durationInSeconds
      } 
    };
    if (
      asset.providerId && asset.title && asset.licensingWindow.start &&
      asset.licensingWindow.end && asset.media.mediaId &&
      asset.media.durationInSeconds &&  asset.profileIds.length
    ) {
      const requestOptions = {
        method: "POST",
        headers: {
          ...authHeader(),
          "Content-type": "application/json"
        },
        body: JSON.stringify(asset)
      }
      const url = `${process.env.REACT_APP_BELL_SERVICE_URL}/bell/hidden/asset/${asset.media.mediaId}`;
  
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
      .then(function() {
        history.push(`/asset/${asset.media.mediaId}`);
      })
      .catch(error => this.setState({ error: error }));
    }
  }

  render() {
    const title = this.state.title;
    const licensingWindowStart = this.state.licensingWindowStart;
    const licensingWindowEnd = this.state.licensingWindowEnd;
    const mediaId = this.state.mediaId;
    const submitted = this.state.submitted;

    const providerValues = this.state.allProviders.map((provider) =>
      <option key={provider.providerId} value={provider.providerId}>{provider.name}</option>
    );

    const profileValues = this.state.allProfiles.map((profile) =>
      <option key={profile.profileId} value={profile.profileId}>{profile.name}</option>
    );

    return (
      <div>
        <section className="section">
          <div className="container">
          {
            this.state.error &&
            <article className="message is-danger">
            <div className="message-body">
              {this.state.error}
            </div>
            </article>
          }

            <div className="columns is-centered">
              <form onSubmit={this.handleSubmit}>
                <h1 className="title has-text-info">
                  Create An Asset
                </h1>

                <div className="field">
                  <p className="control">
                    <input
                      className="input"
                      type="text"
                      placeholder="Media ID"
                      name="mediaId"
                      value={mediaId}
                      onChange={this.onMediaIdChange}/>
                  </p>
                  {(submitted && !mediaId) && 
                    <p className="help is-danger">Please enter a media ID</p>
                  }
                </div>

                <div className="field is-horizontal">
                  <div className="field-label is-normal">
                    <label className="label">Provider</label>
                  </div>
                  <div className="field-body">
                    <div className="field">
                      <div className="control">
                        <div className="select">
                          <select name="providerId" onChange={this.onChange}>
                          { providerValues }
                          </select>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="field">
                  <p className="control">
                    <input
                      className="input"
                      type="text"
                      placeholder="Title"
                      name="title"
                      value={title}
                      onChange={this.onChange}/>
                  </p>
                  {(submitted && !title) && 
                    <p className="help is-danger">Please enter a title</p>
                  }
                </div>

                <div className="field">
                  <label className="label">Licensing Window Start</label>
                  <div className="control">
                    <input
                      className="input"
                      type="date"
                      placeholder="Licensing Window Start"
                      name="licensingWindowStart"
                      value={licensingWindowStart}
                      onChange={this.onChange}/>
                  </div>
                  {(submitted && !licensingWindowStart) && 
                    <p className="help is-danger">Please enter a licensing window start date</p>
                  }
                </div>

                <div className="field">
                  <label className="label">Licensing Window End</label>
                  <div className="control">
                    <input
                      className="input"
                      type="date"
                      placeholder="Licensing Window End"
                      name="licensingWindowEnd"
                      value={licensingWindowEnd}
                      onChange={this.onChange}/>
                  </div>
                  {(submitted && !licensingWindowEnd) && 
                    <p className="help is-danger">Please enter a licensing window end date</p>
                  }
                </div>

                <div className="field">
                  <label className="label">Profiles</label>
                  <div className="field is-narrow">
                    <div className="control is-expanded">
                      <div className="select is-fullwidth is-multiple">
                        <select
                        multiple
                        size={profileValues.length}
                        name="profiles"
                        onChange={this.onSelectChange}>
                          { profileValues }
                        </select>
                      </div>
                    </div>
                    {(submitted && !this.state.profiles.length) &&
                      <p className="help is-danger">Please pick at least one profile</p>
                    }
                  </div>
                </div>

                <div className="field">
                  <p className="control">
                    <button
                    className="button is-success"
                    type="submit">
                      Create Asset
                    </button>
                  </p>
                </div>
              </form>
            </div>
          </div>
        </section>
      </div>
    );
  }
}

export default CreateAsset;
