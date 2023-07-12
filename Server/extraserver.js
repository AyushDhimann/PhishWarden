import express from 'express';
import bodyParser from 'body-parser';
import { spawn } from 'child_process';
import fs from 'fs';
const app = express();
const port = 4000;

// CORS middleware
app.use(function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
  next();
});

// Body parser middleware
app.use(bodyParser.json({ limit: '50mb' }));

app.post('/api', async (req, res) => {
  const { encryptedUrl } = req.body;
  console.log('encryptedUrl:', encryptedUrl);

  // Save the encrypted URL in file.txt
  fs.writeFile('file.txt', encryptedUrl, function (err) {
    if (err) {
      console.error('Error writing to file:', err);
      res.status(500).json({ error: 'Error writing to file' });
      return;
    }
    console.log('Saved encrypted URL in file.txt');
  });

  // Call the Python script to decrypt the URL
  const pythonProcess = spawn('python3', ['Mega.py', encryptedUrl]);

  pythonProcess.on('error', (err) => {
    console.error('Error running Python script:', err);
    res.status(500).json({ error: 'Error running Python script' });
  });

  pythonProcess.on('close', (code) => {
    if (code !== 0) {
      console.error(`Python script exited with code ${code}`);
      res.status(500).json({ error: 'Python script exited with error' });
      return;
    }

    const decryptedUrl = fs.readFileSync('decryptedUrl.txt', 'utf8').trim();
    console.log('decryptedUrl:', decryptedUrl);
    res.json({ decryptedUrl: decryptedUrl });
  });
});

app.listen(port, () => {
  console.log(`Server listening at http://localhost:${port}/api`);
});