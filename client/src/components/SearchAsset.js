import React, { Component } from "react";
import PropTypes from "prop-types";

class SearchAsset extends Component {
  constructor(props) {
    super(props);
    this.state = {
      query: ""
    }
    this.onSubmit = this.onSubmit.bind(this);
  }

  onSubmit = (e) => {
    e.preventDefault();
    this.props.search(this.state.query);
  }

  onChange = (e) => {
    this.setState({
      [e.target.name]: e.target.value
    });
  }

  render() {
    return (
      <section className="section">
        <div className="container">
          <div className="columns is-centered">
            <form onSubmit={this.onSubmit}>
              <div className="field has-addons column">
                <div className="control">
                  <input
                  className="input"
                  type="text"
                  name="query"
                  value={this.state.query}
                  onChange={this.onChange}
                  placeholder="Enter search keywords" />
                </div>

                <div className="control">
                  <button
                  className="button is-info"
                  type="submit">
                    Search
                  </button>
                </div>
              </div>
            </form>
          </div>
        </div>
      </section>
    )
  }
}

SearchAsset.propTypes = {
  search: PropTypes.func.isRequired
}

export default SearchAsset;
