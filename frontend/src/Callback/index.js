import React, { Component } from 'react';

export default class Callback extends Component {

  constructor(props, context) {
    super(props, context)
    this.state = {
      loading: false
    }
  }

  render() {
    const {mood} = this.state;

    return (
        <p>return</p>
    );
  }
}
