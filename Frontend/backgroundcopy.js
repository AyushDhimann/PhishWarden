chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    var tab = tabs[0];
    var url = new URL(tab.url);
    var domainName = url.hostname;
    var filename = domainName + ".txt";



    var blob = new Blob([domainName], {type: "text/plain;charset=utf-8"});
    var urlObject = URL.createObjectURL(blob);
    chrome.downloads.download({url: urlObject, filename: filename});
});
