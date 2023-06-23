import express from 'express';
import bodyParser from 'body-parser';
import fs from 'fs';
import { spawn } from 'child_process';

const app = express();
const port = 4000;

// parse application/json
app.use(bodyParser.json());

// CORS middleware
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept');
  res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  next();
});

// POST endpoint for receiving encrypted URL
app.post('/api', (req, res) => {
  // get the data from the request body
  const data = req.body;

  // write the data to a file called "file.txt"
   fs.writeFile('file.txt', JSON.stringify(data), (err) => {
    if (err) {
      console.error(err);
      res.status(500).json({ error: 'Error writing file' });
    } else {
      console.log('Data written to file');
      res.json({ message: 'Data received and saved to file' });
    }
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
  res.json({ message: 'Data received and saved to file' });
});

app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
