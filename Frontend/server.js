const express = require('express');
const bodyParser = require('body-parser');
const app = express();

// Set up body-parser middleware
app.use(bodyParser.json());

// Define a route to handle incoming POST requests
app.post('/api', (req, res) => {
  // Retrieve the encrypted URL from the request body
  const encryptedUrl = req.body.encryptedUrl;

  // Convert the base64-encoded string to a Uint8Array
  const encryptedData = new Uint8Array(
    atob(encryptedUrl)
      .split('')
      .map((char) => char.charCodeAt(0))
  );

  // Extract the key and IV from the encrypted data
  const key = encryptedData.slice(0, 16);
  const iv = encryptedData.slice(16, 32);
  const data = encryptedData.slice(32);

  // Decrypt the data using AES-CBC
  crypto.subtle.importKey('raw', key, { name: 'AES-CBC' }, false, ['decrypt'])
    .then((aesKey) => crypto.subtle.decrypt({ name: 'AES-CBC', iv: iv }, aesKey, data))
    .then((plaintext) => {
      // Convert the decrypted data to a string
      const domainName = new TextDecoder().decode(plaintext);

      // Send a JSON response with the decrypted domain name
      res.json({ domainName });
    })
    .catch((error) => {
      console.error('Error:', error);
      res.status(500).send('Internal server error');
    });
});

// Start the server on port 3000
app.listen(3000, () => console.log('Server started on port 3000'));


// Just to check if the data is received correctly

// const express = require('express');
// const bodyParser = require('body-parser');
// const app = express();
//
// // Set up body-parser middleware
// app.use(bodyParser.json());
//
// // Define a route to handle incoming POST requests
// app.post('/api', (req, res) => {
//   // Retrieve the encrypted URL from the request body
//   const encryptedUrl = req.body.encryptedUrl;
//
//   console.log('Received encrypted URL:', encryptedUrl);
//
//   // Send a JSON response indicating that the request was successful
//   res.json({ success: true });
// });
//
// // Start the server on port 3000
// app.listen(3000, () => console.log('Server started on port 3000'));
