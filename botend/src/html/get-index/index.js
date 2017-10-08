var arc = require('@architect/functions')
var button = `<a href="https://slack.com/oauth/authorize?&client_id=215690038961.253097127507&scope=bot"><img alt="Add to Slack" height="40" width="139" src="https://platform.slack-edge.com/img/add_to_slack.png" srcset="https://platform.slack-edge.com/img/add_to_slack.png 1x, https://platform.slack-edge.com/img/add_to_slack@2x.png 2x" /></a>`

function route(req, res) {
  res({
    html:button
  })
}

exports.handler = arc.html.get(route)
