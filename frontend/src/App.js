import React, { Component } from 'react';
import logo from './logo.svg';
import axios from 'axios';
import './App.css';

class App extends Component {
  //curl -X POST https://x5p9i5jbd5.execute-api.us-east-1.amazonaws.com/dev/humoji --data '{ "mood": 2}'

  constructor(props, context) {
    super(props, context)
    this.state = {
      loading: false
    }
  }

  doLogin() {
    alert('login');
  }

  doAjax = () => {
    axios.post('https://x5p9i5jbd5.execute-api.us-east-1.amazonaws.com/dev/humoji', {
      mood: 3
    }).then(response => {
      console.log(response.data);
      this.setState(response.data);
    });
  }

  render() {
    const {mood} = this.state;

    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">humoji</h1>
        </header>
        <p className="App-intro">
          <button onClick={this.doLogin}>Login</button>
          <button onClick={this.doAjax}>Ajax</button>
        </p>
        <p>
          {mood}
        </p>
      </div>
    );
  }
}

export default App;
