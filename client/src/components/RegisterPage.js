import React, { Component } from "react";

import uuid from "uuid";

import { connect } from "react-redux";
import { userActions } from "../actions";
import { profileConstants } from "../constants";

class RegisterPage extends Component {
  constructor(props) {
    super(props);

    // reset login status
    this.props.dispatch(userActions.logout());

    this.state = {
      profiles: [],
      username: "",
      password: "",
      submitted: false
    }

    this.onChange = this.onChange.bind(this);
    this.onSelectChange = this.onSelectChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
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
    this.setState({ submitted: true });
    const user = {
      accountId: uuid.v4(),
      profiles: this.state.profiles,
      username: this.state.username,
      password: this.state.password
    };
    const { dispatch } = this.props;
    if (user.profiles.length && user.username && user.password) {
      dispatch(userActions.register(user));
    }
  }

  render() {
    const username = this.state.username;
    const password = this.state.password;
    const submitted = this.state.submitted;

    const profileValues = profileConstants.map((profile) =>
      <option key={profile.profileId} value={profile.name}>{profile.name}</option>
    );

    return (
      <div>
        <section className="section">
          <div className="container">
            <div className="columns is-centered">
              <form onSubmit={this.handleSubmit}>
                <div className="field">
                  <p className="control has-icons-left has-icons-right">
                    <input
                      className="input"
                      type="text"
                      placeholder="Username"
                      name="username"
                      value={username}
                      onChange={this.onChange}/>
                    <span className="icon is-small is-left">
                      <i className="fas fa-user"></i>
                    </span>
                    <span className="icon is-small is-right">
                      <i className="fas fa-check"></i>
                    </span>
                  </p>
                  {(submitted && !username) && 
                    <p className="help is-danger">Please enter a username</p>
                  }
                </div>

                <div className="field">
                  <p className="control has-icons-left">
                    <input
                      className="input"
                      type="password"
                      placeholder="Password"
                      name="password"
                      value={password}
                      onChange={this.onChange}/>
                    <span className="icon is-small is-left">
                      <i className="fas fa-lock"></i>
                    </span>
                  </p>
                  {(submitted && !password) && 
                    <p className="help is-danger">Please enter a password</p>
                  }
                </div>

                <div className="field">
                  <label className="label">Profiles</label>
                </div>

                <div className="field">
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
                  </div>
                </div>

                <div className="field">
                  <p className="control">
                    <button
                    className="button is-success"
                    type="submit">
                      Register
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

function mapStateToProps(state) {
  const { loggingIn } = state.authentication;
  return {
    loggingIn
  };
}

const connectedRegisterPage = connect(mapStateToProps)(RegisterPage);
export {connectedRegisterPage as RegisterPage};
