import React, { Component } from 'react';
import auth0 from 'auth0-js';
import './App.css';
import logo from '../logo.svg';

export default class Shell extends Component {
  //curl -X POST https://x5p9i5jbd5.execute-api.us-east-1.amazonaws.com/dev/humoji --data '{ "mood": 2}'

  constructor(props, context) {
    super(props, context)
    this.state = {
      loading: false
    }
  }

  render() {

    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">humoji</h1>
        </header>
        <p className="App-intro">
        </p>
      </div>
    );
  }
}
