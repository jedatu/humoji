import React, { Component } from 'react';

import face1 from './1.svg';
import face2 from './2.svg';
import face3 from './3.svg';
import face4 from './4.svg';
import face5 from './5.svg';

import axios from 'axios';
import auth0 from 'auth0-js';

export default class Mood extends Component {
  //curl -X POST https://x5p9i5jbd5.execute-api.us-east-1.amazonaws.com/dev/humoji --data '{ "mood": 2}'

  constructor(props, context) {
    super(props, context)
    this.state = {
      loading: false,
      emojis: [
        {id: 1, name: "joy", face: face1 },
        {id: 2, name: "happy", face: face2 },
        {id: 3, name: "satisfied", face: face3 },
        {id: 4, name: "stressed", face: face4 },
        {id: 5, name: "angry", face: face5 }
      ]
    }
  }

  doAjax = (id) => {
    axios({
      method: 'post',
      url: 'https://x5p9i5jbd5.execute-api.us-east-1.amazonaws.com/dev/humoji',
      data: {
        mood: id
      },
      headers: {
        Authorization: 'Bearer ' + window.localStorage.getItem('id_token')
      }
    }).then(response => {
      console.log(response.data);
      this.setState(response.data);
    });
  }

  renderEmojis() {
    return this.state.emojis.map((emoji, n) => {
      return (<img key={emoji.id}
        style={{width:'10%', padding:'10px'}}
        onClick={this.doAjax.bind(this, emoji.id)}
        alt={emoji.name} src={emoji.face} />);
    });
  }

  render() {
    const {mood} = this.state;

    return (
        <p className="App-intro">
            {this.renderEmojis()}
        </p>
    );
  }
}
