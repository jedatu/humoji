
let callbackUrl = 'http://localhost:3000/callback'
if (process.env.NODE_ENV === 'production') {
  callbackUrl = 'https://humoji.surge.sh/callback'
}

export const AUTH_CONFIG = {
    domain: 'jedatu.auth0.com',
    clientID: 'qVdbj7FwKWAO625Fk7g0e6WOhAwdi6Q8',
    callbackUrl: callbackUrl
}