import React from 'react'
import { Route, Router, Switch, Redirect } from 'react-router-dom'
import App from './App'
import Mood from './Mood'
import Login from './Login'
import Welcome from './Welcome'

import Callback from './Callback'
import Auth from './utils/Auth'
import history from './utils/history'

const auth = new Auth()

const handleAuthentication = (nextState, replace) => {
    if (/access_token|id_token|error/.test(nextState.location.hash)) {
        auth.handleAuthentication()
    }
}

export const makeMainRoutes = () => {
    const homeRedirect = <Redirect to="/" />
    const home = (props) => !auth.isAuthenticated() ? homeRedirect : <Mood auth={auth} {...props} />
    const mood = (props) => !auth.isAuthenticated() ? homeRedirect : <Mood auth={auth} {...props} />

    return (
        <Router history={history} component={App}>
            <div className="app-contents">
                <Route path="/" render={(props) => <App auth={auth} {...props} />} />
                <Switch>
                    <Route path="/" exact render={(props) => <Welcome auth={auth} {...props} />} />
                    <Route path="/mood" exact render={mood} />
                    <Route path="/callback" render={(props) => {
                        handleAuthentication(props);
                        return <Callback {...props} />
                    }} />
                </Switch>
            </div>
        </Router>
    );
}