var tiny = require('tiny-json-http')

exports.handler = function _event(event, context, callback) {

  var url = 'https://x5p9i5jbd5.execute-api.us-east-1.amazonaws.com/dev/humoji'
  var allowed = [':angry:', ':cry:', ':neutral_face:', ':slightly_smiling_face:', ':smile:']
  var mood = allowed.indexOf(event.text)

  if (!allowed.includes(event.text)) {
    var text = 'sorry that is an invalid emotion'
    callback(null, {text})
  }
  else {
    tiny.post({
      url, 
      data: {mood}
    },
    function _post(err, res) {
      if (err) {
        var text = err
      }
      else {
        var text = 'thx'
      }
      callback(null, {text})
    })
  }
}
