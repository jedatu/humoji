import React, { Component } from 'react';
import { Link } from 'react-router-dom';

export default class Welcome extends Component {

  constructor(props, context) {
    super(props, context)
    this.state = {
      loading: false
    }
  }

  render() {
    const {mood} = this.state;

    return (
        <div>
            <h1 style={{textAlign:'center'}}>Welcome</h1>
            <p style={{textAlign:'center'}}><Link to="/mood">Record your mood!</Link></p>
        </div>
    );
  }
}
