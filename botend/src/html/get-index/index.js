var arc = require('@architect/functions')
var slack = require('slack')
var button = `<a href="https://slack.com/oauth/authorize?&client_id=215690038961.253097127507&scope=bot,commands"><img alt="Add to Slack" height="40" width="139" src="https://platform.slack-edge.com/img/add_to_slack.png" srcset="https://platform.slack-edge.com/img/add_to_slack.png 1x, https://platform.slack-edge.com/img/add_to_slack@2x.png 2x" /></a>`

function route(req, res) {
  if (req.query.code) {
    // auth slack???
    slack.oauth.access({
      code: req.query.code,
      client_id: process.env.SLACK_CLIENT_ID,
      client_secret: process.env.SLACK_CLIENT_SECRET,
    }, 
    function _access(err, result) {
      if (err) {
        res({
          html: `Uh oh. Something went wrong. <pre>${JSON.stringify(result, null, 2)}</pre>`
        })
      }
      else {
        res({
          html: 'success!!'
        }) 
      }
    })
  }
  else {
    res({
      html: button
    })
  }
}

exports.handler = arc.html.get(route)
