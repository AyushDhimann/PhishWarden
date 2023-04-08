chrome.tabs.query({active: true, currentWindow: true}, async function (tabs) {
    if (tabs.length === 0) {
        console.error('No active tabs found');
        return;
    }
    var tab = tabs[0];
    if (!tab.url) {
        return;
    }
    var url = new URL(tab.url);
    var domainName = url.hostname;
    var plainText = domainName;

    // Generate a custom key
    var customKey = "1234567890123456";

    // Encoding the Key
    var key = new TextEncoder().encode(customKey);

    // Encrypt the plaintext with AES-CBC
    // var iv = crypto.getRandomValues(new Uint8Array(16));
    var iv = new TextEncoder().encode(customKey);
    var aesKey = await crypto.subtle.importKey("raw", key, { name: "AES-CBC" }, false, ["encrypt"]);
    var encryptedData = await crypto.subtle.encrypt(
        { name: "AES-CBC", iv: iv },
        aesKey,
        new TextEncoder().encode(plainText)
    );

    // Concatenate the key and IV to the encrypted data
    var encrypted = new Uint8Array(key.length + iv.length + encryptedData.byteLength);
    encrypted.set(key);
    encrypted.set(iv, key.length);
    encrypted.set(new Uint8Array(encryptedData), key.length + iv.length);

    // Convert the encrypted data to a base64-encoded string
    var base64Encrypted = btoa(String.fromCharCode.apply(null, encrypted));

    try {
        const headers = {'Content-Type':'application/json'}
        const body = { encryptedUrl: base64Encrypted }
        const options = {
            method: 'POST',
            headers: headers,
            mode: 'cors',
            credentials: 'same-origin',
            body: JSON.stringify(body) // pass encryptedUrl in the request body
        };
        const response = await fetch('http://pawbox.me:4000/api', options);
        // Parse the JSON response
        const responseData = await response.json();
        console.log(responseData);
    } catch (error) {
        // console.error('Error:', error);
    }

    // Update the content of the HTML elements with the encrypted URL and domain name
    document.getElementById("encrypted-url").textContent = base64Encrypted;
    document.getElementById("domain-name").textContent = domainName;
    document.getElementById("IV").textContent = iv;
    document.getElementById("BODY").textContent = base64Encrypted;
});
