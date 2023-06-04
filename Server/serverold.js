// sudo apt-get install nodejs
// sudo apt-get install npm
// npm install express
// npm install body-parser
// make sure it is placed in the server directory
// node server.js

import express from 'express';
import bodyParser from 'body-parser';
import fs from 'fs';
import { spawn } from 'child_process';

const app = express();
const port = 4000;

// parse application/json
app.use(bodyParser.json());

// POST endpoint for receiving encrypted URL
app.post('/api', (req, res) => {
  // get the data from the request body
  const data = req.body;

  // write the data to a file called "file.txt"
  fs.writeFile('file.txt', JSON.stringify(data), (err) => {
    if (err) throw err;
    console.log('Data written to file');
  });

  // spawn a child process to execute the Python script
  const ls = spawn('python3', ['Mega.py']);

  // listen for stdout and stderr output from the script
  ls.stdout.on('data', (data) => {
    console.log(`stdout: ${data}`);
  });

  ls.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
  });

  // send a response to the client
  res.send('Data received and saved to file');
});

app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
