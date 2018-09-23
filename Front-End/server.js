// Reference: https://github.com/mschwarzmueller/nodejs-basics-tutorial/blob/master/03-node-only-render-html/server.js
var http = require('http');
var fs = require('fs');

function onRequest(request, response) {
    response.writeHead(200, {'Content-Type': 'text/html'});
    // Reading the data in the file mentioned
    fs.readFile('./homepage.html', null, function(error, data) {

        // Handling the case in which no file with the given name is found
        if (error) {
            response.writeHead(404);
            response.write('File not found!');
        }
        // If the file is found, the data in the file is supposed to be written
        else {
            response.write(data);
        }
        response.end();
    });
}

http.createServer(onRequest).listen(8000);
