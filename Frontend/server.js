const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');
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

  // send a response to the client
  res.send('Data received and saved to file');
});

app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
