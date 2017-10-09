const lib = require('lib');

/**
* Basic "Hello World" intent, can receive a `name` parameter
* @param {string} Mood Your name
* @returns {string}
*/
module.exports = (Mood = 'happy', context, callback) => {
    console.log(context);

    let moods = {
        "great": "Super!, glad to hear it.",
        "happy": "Thats great",
        "okay": "Hmmm indecisive today",
        "sad": "Sometimes it happens",
        "angry": "You must not be at serverless conference"
    };

    let mood = (moods[Mood] || "I can not explain that");

    return callback(null, mood);

};
