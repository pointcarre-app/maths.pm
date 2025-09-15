const http = require('http');
const fs = require('fs');
const path = require('path');

const server = http.createServer((req, res) => {
    const defaultFile = 'capture-identity.html';
    const filePath = path.join(__dirname, req.url === '/' ? defaultFile : req.url);
    
    if (fs.existsSync(filePath)) {
        const ext = path.extname(filePath);
        const contentType = ext === '.html' ? 'text/html' : 
                           ext === '.css' ? 'text/css' : 'text/plain';
        
        res.writeHead(200, { 'Content-Type': contentType });
        fs.createReadStream(filePath).pipe(res);
    } else {
        res.writeHead(404);
        res.end('Not found');
    }
});

server.listen(3000, () => console.log('Server running on http://localhost:3000'));
