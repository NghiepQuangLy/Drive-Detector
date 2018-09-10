/*
const http = require('http');

const hostname = '127.0.0.1';
const port = 3000;

const server = http.createServer((req, res) => {
  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/plain');
  // res.end('Hello World\n');
  // res.end(trial.html);

  app.get('/', function (req, res){

    // make the call to twitter before sending the response
    var options = { q: hash1 + ' since:2013-11-11', count: 5 };
    T.get('search/tweets', options, function(err, reply) {
      // use RENDER instead of SENDFILE
      res.render('./trial.html', {data: reply});
    });
});


});
server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});*/
var http = require('http');
var fs = require('fs');

function onRequest(request, response) {
    response.writeHead(200, {'Content-Type': 'text/html'});
    fs.readFile('./index.html', null, function(error, data) {
        if (error) {
            response.writeHead(404);
            response.write('File not found!');
        } else {
            response.write(data);
        }
        response.end();
    });
}

http.createServer(onRequest).listen(8000);
