import React, { Component } from 'react';
import Notifications, {notify} from 'react-notify-toast';
import logo from './Mood/1.svg';
import Login from './Login'
import Logout from './Logout'

import axios from 'axios';
import auth0 from 'auth0-js';
import './App.css';

class App extends Component {
  //curl -X POST https://x5p9i5jbd5.execute-api.us-east-1.amazonaws.com/dev/humoji --data '{ "mood": 2}'

  constructor(props, context) {
    super(props, context)
    this.state = {
      loading: false
    }
  }

  doAjax = (id) => {
    axios.post('https://x5p9i5jbd5.execute-api.us-east-1.amazonaws.com/dev/humoji', {
      mood: id
    }).then(response => {
      console.log(response.data);
      this.setState(response.data);
    });
  }


  render() {
    const {mood} = this.state;

    let button;
    if (!this.props.auth.isAuthenticated()) {
      button = <Login auth={this.props.auth} />
    } else {
      button = <Logout auth={this.props.auth} />
    }

    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">humoji</h1>
          {button}
        </header>
        <Notifications />
        <p className="App-intro">

        </p>
      </div>
    );
  }
}

export default App;
