'use strict';

// module.exports.hello = (event, context, callback) => {
//   const response = {
//     statusCode: 200,
//     body: JSON.stringify({
//       message: 'Go Serverless v1.0! Your function executed successfully!',
//       input: event,
//     }),
//   };
// 
//   callback(null, response);
// 
//   // Use this code if you don't use the http event with the LAMBDA-PROXY integration
//   // callback(null, { message: 'Go Serverless v1.0! Your function executed successfully!', event });
// };

var http = require('http');

module.exports.iotclick = (event, context, callback) => {
  console.log({
    event: JSON.stringify(event)
  });

//   var postOptions = {
//     method: 'POST',
//     hostname: process.env.API_HOST,
//     path: `/api/buttons/${event.serialNumber}/trigger`,
//     headers: {
//       "Accept": "application/json" //,
//     //   "X-Coupa-Api-Key": process.env.API_KEY
//     }
//   };

//   var req = http.request(postOptions);
//   req.on('error', (e) => {
//     console.log(`problem with request: ${e.message}`);
//   });
//   req.end();
};