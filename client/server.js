const express = require('express');
const http = require('http');
const path = require('path');
const reload = require('reload');
const bodyParser = require('body-parser');
const logger = require('morgan');
const { createProxyMiddleware } = require('http-proxy-middleware');

// const app = express();

//拦截 访问 http://backend:8000/ 的请求，变成 http://localhost:3000/api/
const apiProxy = createProxyMiddleware('http://backend:8000/', {
  target: 'http://localhost:3000/api/',
  changeOrigin: true,
  // pathRewrite: {
  //   '^/api': '', // remove base path
  // },

});
// const apiProxy = createProxyMiddleware('/api', {
//   target: 'http://47.110.131.191:3000', // replace with your API server
//   changeOrigin: true, // needed for virtual hosted sites
//   ws: true, // proxy websockets
//   // pathRewrite: {
//   //   '^/api': '', // remove base path
//   // },
// });

// // Apply proxy to express app

app.use(apiProxy);

app.set('port', process.env.PORT || 3000);
app.use(logger('dev'));
app.use(bodyParser.json()); // Parses json, multi-part (file), url-encoded

app.use('/public', express.static('public'));
app.use('/pages', express.static('pages'));
app.use('/sdk', express.static('amis/sdk'));

app.get('/*', function (req, res) {
  res.sendFile(path.join(__dirname, 'index.html'));
});

const server = http.createServer(app);

// Reload code here
reload(app,{port:app.get('port')+1})
  .then(function (reloadReturned,) {
    // reloadReturned is documented in the returns API in the README

    // Reload started, start web server
    server.listen(app.get('port'), function () {
      console.log(
        'Web server listening on port http://localhost:' + app.get('port')
      );
    });
  })
  .catch(function (err) {
    console.error(
      'Reload could not start, could not start server/sample app',
      err
    );
  });
