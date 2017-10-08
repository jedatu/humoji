import React, { Component } from 'react';

import auth0 from 'auth0-js';

export default class Login extends Component {

  constructor(props, context) {
    super(props, context)
    this.state = {
      loading: false
    }
  }

  render() {
    const {mood} = this.state;

    return (
        <button onClick={this.props.auth.logout}>Logout</button>
    );
  }
}
