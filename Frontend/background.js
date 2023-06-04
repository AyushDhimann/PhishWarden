chrome.tabs.query({active: true, currentWindow: true}, async function (tabs) {
    console.log("tabs:", tabs);

    if (tabs.length === 0) {
        console.error('No active tabs found');
        return;
    }
    var tab = tabs[0];
    if (!tab.url) {
        console.log('Tab has no URL');
        return;
    }
    var url = new URL(tab.url);
    var domainName = url.hostname;
    console.log("domainName:", domainName);
    var plainText = domainName;

    // Generate a custom key
    var customKey = "1234567890123456";
    console.log("customKey:", customKey);

    // Encoding the Key
    var key = new TextEncoder().encode(customKey);
    console.log("key:", key);

    // Encrypt the plaintext with AES-CBC
    // var iv = crypto.getRandomValues(new Uint8Array(16));
    var iv = new TextEncoder().encode(customKey);
    console.log("iv:", iv);
    var aesKey = await crypto.subtle.importKey("raw", key, { name: "AES-CBC" }, false, ["encrypt"]);
    var encryptedData = await crypto.subtle.encrypt(
        { name: "AES-CBC", iv: iv },
        aesKey,
        new TextEncoder().encode(plainText)
    );
    console.log("encryptedData:", encryptedData);

    // Concatenate the key and IV to the encrypted data
    var encrypted = new Uint8Array(key.length + iv.length + encryptedData.byteLength);
    encrypted.set(key);
    encrypted.set(iv, key.length);
    encrypted.set(new Uint8Array(encryptedData), key.length + iv.length);
    console.log("encrypted:", encrypted);

    // Convert the encrypted data to a base64-encoded string
    var base64Encrypted = btoa(String.fromCharCode.apply(null, encrypted));
    console.log("base64Encrypted:", base64Encrypted);

    try {
        const headers = {'Content-Type':'application/json'}
        const body = { encryptedUrl: base64Encrypted }
        const options = {
            method: 'POST',
            headers: headers,
            // mode: 'no-cors',
            credentials: 'same-origin',
            body: JSON.stringify(body) // pass encryptedUrl in the request body
        };
        console.log("options:", options);
        const response = await fetch('https://eokdhydqf6vxow0.m.pipedream.net', options);
        console.log("response:", response);
        // Parse the JSON response
        const responseData = await response.json();
        console.log("responseData:", responseData);

        // Decrypt the URL
        var encryptedResult = responseData.encryptedUrl;
        console.log("encryptedResult:", encryptedResult);
        var rencrypted = new Uint8Array(atob(encryptedResult).split("").map(function(c) { return c.charCodeAt(0); }));
        var rkey = rencrypted.slice(0, 16);
        var riv = rencrypted.slice(16, 32);
        var rdata = rencrypted.slice(32);
        var raesKey = await crypto.subtle.importKey("raw", rkey, { name: "AES-CBC" }, false, ["decrypt"]);
        var decryptedData = await crypto.subtle.decrypt(
            { name: "AES-CBC", iv: riv },
            raesKey,
            rdata
        );
        var isLegitimate = new TextDecoder().decode(decryptedData);
        console.log("decryptedUrl:", isLegitimate);

        // Update the content of the HTML elements with the encrypted URL, domain name, and decrypted URL
        document.getElementById("encrypted-url").textContent = base64Encrypted;
        document.getElementById("domain-name").textContent = domainName;
        document.getElementById("IV").textContent = iv;
        document.getElementById("BODY").textContent = base64Encrypted;
        document.getElementById("isLegitimate").textContent = isLegitimate;
    } catch (error) {
        // console.error('Error:', error);
    }
});
