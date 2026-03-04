# PhishWarden

> A real-time phishing detection system powered by a Chrome extension, a Node.js API gateway, and a Random Forest machine learning model trained on live-scraped URL intelligence.

---

## Table of Contents

- [What Is PhishWarden?](#what-is-phishwarden)
- [The Problem It Solves](#the-problem-it-solves)
- [High-Level Architecture](#high-level-architecture)
- [How It Works — End to End](#how-it-works--end-to-end)
  - [1. The Browser Extension (Frontend)](#1-the-browser-extension-frontend)
  - [2. The API Gateway (Server)](#2-the-api-gateway-server)
  - [3. The Feature Scraper](#3-the-feature-scraper)
  - [4. The ML Inference Engine](#4-the-ml-inference-engine)
  - [5. The Response Journey Back](#5-the-response-journey-back)
- [Machine Learning: Inside the Model](#machine-learning-inside-the-model)
  - [Features Used](#features-used)
  - [Why Random Forest?](#why-random-forest)
  - [Training Pipeline](#training-pipeline)
- [Dataset Creation Pipeline](#dataset-creation-pipeline)
- [SimilarFinder: Typosquatting Detection](#similarfinder-typosquatting-detection)
- [Encryption Layer: Why AES-CBC?](#encryption-layer-why-aes-cbc)
- [Design Decisions & Rationale](#design-decisions--rationale)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [Potential & Roadmap](#potential--roadmap)

---

## What Is PhishWarden?

PhishWarden is an end-to-end anti-phishing system that intercepts a user's browsing activity at the browser level, extracts intelligence about each visited domain in real time, runs it through a trained machine learning classifier, and reports back whether the site is likely a phishing page — all within the time it takes the user to load a page.

The project is not just a URL blocklist lookup. It performs **live, active analysis** of a domain: checking its SSL certificate, querying its WHOIS registration age, scraping its content for known scam vocabulary, and checking its HTTP response — then feeding all of that contextual data into a classifier trained on thousands of verified phishing and legitimate URLs.

---

## The Problem It Solves

Phishing attacks remain one of the most effective and damaging vectors in cybersecurity. Attackers register domains that look legitimate, spin them up within hours of a campaign launch, and take them down just as fast — making static blocklists perpetually behind. Standard browser protection is reactive; it blocks known-bad URLs only after they've been reported and indexed.

PhishWarden's goal is to shift from **"is this URL on a known list?"** to **"does this URL exhibit the behaviour of a phishing site right now?"** by evaluating live signals.

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    CHROME BROWSER                               │
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  Extension (Manifest V3)                               │    │
│  │  • Captures current tab's domain                       │    │
│  │  • AES-CBC encrypts the domain name                    │    │
│  │  • POSTs encrypted payload to API server               │    │
│  │  • Decrypts and displays "safe / phishing" verdict     │    │
│  └─────────────────────────┬──────────────────────────────┘    │
└────────────────────────────│────────────────────────────────────┘
                             │ HTTPS POST (encrypted payload)
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  Node.js Express Server  (port 4000)                           │
│  • Receives encrypted domain name                              │
│  • Writes to file.txt                                          │
│  • Spawns Python child process (Mega.py)                       │
│  • Returns encrypted verdict                                   │
└─────────────────────────────┬───────────────────────────────────┘
                              │ child_process.spawn
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Python Backend (Mega.py)                                       │
│                                                                 │
│  ┌──────────────┐    ┌──────────────────────────────────────┐  │
│  │  Decrypt.py  │    │  Scraper.py                          │  │
│  │  Reads URL   │───▶│  • SSL check                         │  │
│  │  from file   │    │  • WHOIS domain age                  │  │
│  └──────────────┘    │  • HTTP status code                  │  │
│                      │  • Blacklisted keyword scan           │  │
│                      └──────────────────┬───────────────────┘  │
│                                         │ feature vector        │
│                                         ▼                       │
│                      ┌──────────────────────────────────────┐  │
│                      │  Random Forest Classifier            │  │
│                      │  (phishing_model.joblib)             │  │
│                      │  → predicts: phishing / legitimate   │  │
│                      └──────────────────┬───────────────────┘  │
│                                         │                       │
│                      ┌──────────────────▼───────────────────┐  │
│                      │  Encrypt.py                           │  │
│                      │  Encrypts "yes"/"no" result           │  │
│                      └──────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## How It Works — End to End

### 1. The Browser Extension (Frontend)

The Chrome extension is built to **Manifest V3**, using a service worker (`background.js`) and a popup (`popup.html`). The extension activates when the user opens the popup from the browser toolbar.

**What it does:**
1. Queries the current active tab for its URL.
2. Extracts just the **hostname** (domain name), e.g. `evil-bank-login.com`.
3. Encrypts the hostname using **AES-CBC** with a symmetric key (`background55.js` - the production version sends only the domain; `background.js` - a development version sent the full URL).
4. Base64-encodes the encrypted bytes (including the prepended key and IV).
5. POSTs the base64 string as JSON to the backend API: `POST /api { encryptedUrl: "..." }`.
6. Awaits the response, then decrypts the returned verdict and displays it in the popup.

The popup currently shows: encrypted URL, domain name, IV, body payload, and the `isSafe` verdict — these debug fields are intentional artefacts of active development.

**Why encrypt at the browser level?** The server was deployed over plain HTTP (port 4000). Sending a domain name in plaintext over HTTP broadcasts exactly which sites a user is visiting to any network observer. Encrypting it before sending — even with a symmetric key — prevents trivial eavesdropping at the transport layer. It is a partial measure that would be fully resolved by deploying the server with TLS.

---

### 2. The API Gateway (Server)

`Server/server.js` is a minimal **Node.js + Express** application running on port 4000. It has a single POST endpoint at `/api`.

**What it does:**
1. Receives the JSON body `{ encryptedUrl: "<base64 string>" }`.
2. Writes it to `file.txt` on disk.
3. Uses `child_process.spawn` to launch `python3 Mega.py` as a subprocess.
4. Streams the Python process's stdout/stderr to its own console for logging.
5. Sends an immediate `{ message: "Data received and saved to file" }` response back to the browser.

**Why Node.js as the gateway?** The browser extension can only communicate with HTTP(S) endpoints. Node.js is the natural choice for writing a fast, non-blocking API layer. It also decouples the browser-facing interface from the Python ML backend cleanly — Node handles the network I/O while Python handles the computation. The `child_process.spawn` approach means the Python interpreter is loaded fresh per request, which keeps the server stateless and easy to reason about.

**Limitation / Growth area:** The current design has the Node.js server respond *before* the Python script completes, and the result is printed to stdout rather than returned in the HTTP response. The newer `Mega.py` iteration pipes the encrypted result back through `Encrypt.py` for a round-trip delivery. Connecting the Python stdout back to the HTTP response (or using a message queue) is the clear next evolution.

---

### 3. The Feature Scraper

`Server/Scraper.py` is the intelligence-gathering module. Given a domain name, it extracts a multi-dimensional feature vector:

| Feature | How It's Gathered | Why It Matters |
|---|---|---|
| **URL itself** | Raw string | URL structure (length, suspicious keywords in path) carries signal |
| **SSL certificate** | HTTPS request, checking response.ok | Phishing sites commonly skip SSL or use free-tier certs |
| **Domain age (days)** | `python-whois` WHOIS lookup | Phishing domains are typically registered hours/days before a campaign; legitimate domains are months to years old |
| **HTTP status code** | HTTP GET request | Legitimate sites return 200; abandoned or placeholder phishing pages often return 4xx/5xx |
| **Blacklisted words** | Full page content scan | Phishing pages reliably contain certain vocabulary: `login`, `verify`, `account`, `bitcoin`, `secure`, brand names like `paypal`, `microsoft`, etc. |

The blacklist is a curated list of ~60 terms covering financial fraud, cryptocurrency scams, social engineering vocabulary, and brand impersonation.

The scraper also collects secondary signals (IP address, iframes count, nameservers, URL length) which are available for future feature expansion.

---

### 4. The ML Inference Engine

`Server/Mega.py` is the orchestrator for inference:

1. Calls `Decrypt.py` to read and decrypt the URL from `file.txt`.
2. Imports the extracted feature variables from `Scraper.py` (`url`, `ssl`, `age`, `status_code`, `blacklisted_words`).
3. Loads the pre-trained `phishing_model.joblib` (the saved Random Forest model).
4. Applies the same preprocessing pipeline used during training (StandardScaler on numerics, OneHotEncoder on URL, CountVectorizer on blacklisted words text).
5. Calls `clf.predict()` to get a binary prediction: `1` = phishing, `0` = legitimate.
6. Encrypts the string result (`"yes"` or `"no"`) with `Encrypt.py` and prints it.

---

### 5. The Response Journey Back

The encrypted verdict (`"yes"` or `"no"` encrypted with AES-CBC, base64 encoded) flows back:

```
Python prints encrypted result
  → Node.js captures stdout
    → Node.js sends it in the HTTP response body as { decryptedUrl: "<encrypted result>" }
      → Browser JavaScript decrypts it
        → Popup displays "isSafe: yes/no"
```

Note: the field name `decryptedUrl` in the response is a naming artefact — it actually carries the encrypted prediction result which the browser then decrypts. The naming reflects it being "the thing that gets decrypted client-side."

---

## Machine Learning: Inside the Model

### Features Used

```
url               → the domain string
ssl               → 1 (SSL present) or 0 (no SSL) — boolean
age               → number of days since domain registration
status_code       → HTTP response code (200, 403, 404, etc.)
blacklisted_words → space-separated string of matching scam keywords found on the page
label             → 1 (phishing) or 0 (legitimate) — training target
```

### Why Random Forest?

Random Forest was selected over alternatives for several concrete reasons:

1. **Tabular structured data.** The feature set is a mix of numeric (age, status_code), boolean (ssl), encoded categorical (url), and text (blacklisted_words). Random Forest handles heterogeneous feature types well with appropriate preprocessing. Deep learning would require far more data to outperform it here.

2. **Ensemble robustness.** 100 decision trees vote on the outcome. A single tree would overfit easily on a dataset where one feature (e.g. age) may dominate. The ensemble averages out variance from individual trees.

3. **Resistance to overfitting** via bootstrap aggregation (bagging) and random feature subsets at each split. This is critical for security use-cases where the training distribution never perfectly matches the future real-world distribution of phishing domains.

4. **No scaling required for tree splits.** While StandardScaler is applied (and is the correct practice for the preprocessing pipeline's consistency), tree-based methods are inherently invariant to feature magnitude — making the model more forgiving of preprocessing imperfections.

5. **Speed.** Inference on a single URL is near-instant once the model is loaded. This is crucial for a real-time browser tool.

6. **Interpretability.** Feature importances can be extracted from the trained forest, which is valuable for auditing why a domain was flagged.

### Training Pipeline

```python
# Preprocessing
numerical:    StandardScaler        → ['ssl', 'age', 'status_code']
categorical:  OneHotEncoder         → ['url']
text:         CountVectorizer       → 'blacklisted_words'

# Combined via ColumnTransformer → Random Forest (n_estimators=100, random_state=42)
```

The trained model is serialised with `joblib` to `phishing_model.joblib` and loaded at inference time without re-training.

---

## Dataset Creation Pipeline

Building the training data requires scraping and labelling hundreds of URLs. The pipeline is:

```
Backend/AIO/aio.py  (orchestrator)
    │
    ├── datain.py         → Downloads PhishTank's online-valid.csv
    │                       (crowd-sourced, human-verified phishing URLs)
    │
    ├── cleaner.py        → Strips malformed rows, normalises URL format
    │
    ├── file_slicer.py    → Splits large URL lists into manageable chunks
    │                       for parallel processing
    │
    ├── cleaning_csv.py   → Post-scrape data cleaning, removes nulls,
    │                       handles failed lookups
    │
    └── scrapper.py       → Multithreaded URL feature scraper
                            Extracts: IP, iframes, age, SSL,
                            blacklisted_words, nameservers, status_code, length
                            Writes labelled rows to Scraped.csv
```

**PhishTank** (`http://data.phishtank.com/data/online-valid.csv`) provides the phishing ground truth — a publicly available, continuously updated feed of verified phishing URLs. Using a community-verified source is important: it means each labelled sample has been reviewed by multiple human analysts, not just a heuristic.

Legitimate URLs are sourced separately (e.g. from Alexa top-site lists) and merged with the phishing URLs before shuffling (`Shuffled.csv`) to create a balanced binary classification dataset.

The `ScraperNew.py` file is an experimental multithreaded rewrite using `ThreadPoolExecutor` for faster parallel feature extraction across large URL batches — the existing scraper processes URLs sequentially, which is the main bottleneck in dataset creation.

---

## SimilarFinder: Typosquatting Detection

`Backend/SimilarFinder/` is an orthogonal detection module targeting a specific attack type: **typosquatting** — registering domains that look visually similar to trusted brands, e.g. `paypa1.com`, `g00gle.com`, `amaz0n-deals.net`.

**How it works:**

1. `Splitter.py` pre-processes a large reference corpus (`large_file.txt`, containing hundreds of thousands of legitimate domain names) by splitting it alphabetically into 37 files (`a.txt` through `z.txt`, `0.txt` through `9.txt`).

2. `Searcher.py` takes a target domain as input, reads only the file matching the target's first character (dramatically reducing the search space), then computes the **Levenshtein distance** between the target and every domain in that file.

3. Using a min-heap (`heapq.nsmallest`), it returns the top 3 closest known-legitimate domains.

**Why Levenshtein distance?** It counts the minimum number of single-character edits (insertions, deletions, substitutions) to transform one string into another. A phishing domain like `paypa1.com` has a Levenshtein distance of 1 from `paypal.com` — immediately identifiable as suspicious. It requires no training, no model, and runs in microseconds per comparison.

**The alphabetic pre-split is a key optimisation.** The full domain list may contain 500,000+ entries. Comparing against all of them for every lookup would be slow. By splitting on the first character, the average comparison count drops by a factor of ~36. This makes real-time typosquatting detection practical.

The potential of this module is to be combined with the ML classifier: if the ML model flags a site as suspicious AND the SimilarFinder shows it is one edit away from a known brand, confidence in the phishing verdict increases substantially.

---

## Encryption Layer: Why AES-CBC?

All URL data transmitted between the browser extension and the server is encrypted using **AES-CBC (Advanced Encryption Standard in Cipher Block Chaining mode)**.

**The specific implementation:**
- Key: `"1234567890123456"` (16-byte ASCII string → 128-bit AES key)
- IV: same as the key (also 16 bytes) — used for the CBC initialisation vector
- The final payload is: `base64(key_bytes + iv_bytes + ciphertext)`
- The receiver can extract the key and IV from the first 32 bytes, then decrypt

**Why AES-CBC and not just HTTPS?** The server was running on HTTP, not HTTPS. While the long-term fix is TLS on the server, AES-CBC was implemented as an application-layer encryption layer to prevent the domain names from being visible to any network intermediary in plaintext. It was a pragmatic, immediately deployable privacy measure.

**Known limitation:** The encryption key is hardcoded and symmetric. Both sides share the same static key, which means anyone who reads the source code can decrypt the payload. This is appropriate for a research/prototype system but would need to be replaced with proper key management (e.g. a server-side key rotation or asymmetric encryption for key exchange) before any production deployment.

---

## Design Decisions & Rationale

| Decision | Rationale |
|---|---|
| Chrome Extension (Manifest V3) | Direct integration into the browsing experience; no user action required beyond installing the extension. MV3 is the current Chrome standard with a service worker model. |
| Node.js API gateway + Python ML backend | Each language is used for what it does best: Node handles non-blocking HTTP I/O; Python has the mature ML ecosystem (scikit-learn, pandas, joblib). They communicate via child process and file I/O. |
| Random Forest over deep learning | The feature set is small and tabular. Deep learning would overfit on small datasets and add unnecessary complexity and latency. RF achieves high accuracy with interpretable internals. |
| PhishTank as ground truth | Crowd-sourced and continuously updated, human-verified phishing URL database. Far more reliable than heuristically labelled data. |
| Live feature extraction (not cached) | Phishing sites change rapidly. Checking SSL, age, and content at query time means the model sees the site's current state, not a stale snapshot. |
| Alphabetic split for SimilarFinder | Reduces Levenshtein search space by ~36x, making real-time typosquatting detection practical on large domain corpora. |
| AES-CBC for in-transit encryption | Provides application-layer privacy over plain HTTP without requiring infrastructure changes to add TLS. Symmetric key is a known limitation to be addressed. |

---

## Project Structure

```
PhishWarden/
├── Frontend/                   # Chrome Extension
│   ├── manifest.json           # Extension manifest (MV3)
│   ├── popup.html              # Extension popup UI
│   ├── background.js           # Dev version: encrypts full URL
│   ├── background55.js         # Production version: encrypts domain only
│   └── server.js               # Frontend dev/test server
│
├── Server/                     # Deployed API Backend
│   ├── server.js               # Node.js Express API (port 4000)
│   ├── Mega.py                 # ML inference orchestrator
│   ├── Scraper.py              # Live URL feature extraction
│   ├── Encrypt.py              # AES-CBC encryption (Python)
│   ├── Decrypt.py              # AES-CBC decryption (Python)
│   ├── phishing_model.joblib   # Trained Random Forest model
│   └── Shuffled.csv            # Training dataset (reference copy)
│
├── Backend/
│   ├── AIO/                    # All-in-one dataset creation pipeline
│   │   ├── aio.py              # Pipeline orchestrator
│   │   ├── datain.py           # Downloads PhishTank CSV
│   │   ├── cleaner.py          # Data cleaning
│   │   ├── file_slicer.py      # Splits large URL lists
│   │   ├── cleaning_csv.py     # Post-scrape CSV cleanup
│   │   └── scrapper.py         # Multithreaded feature scraper
│   │
│   ├── Dataset_Creation/       # Dataset building scripts
│   │   ├── Scraper.py          # Original sequential scraper
│   │   ├── ScraperNew.py       # Experimental multithreaded scraper
│   │   ├── Dataset_Creator.py  # CSV assembly
│   │   └── url.txt             # Input URL list
│   │
│   ├── Dataset_Files/          # Training data at various stages
│   │   ├── online-valid.csv    # Raw PhishTank phishing URLs
│   │   ├── Shuffled.csv        # Final balanced training dataset
│   │   └── ...                 # Intermediate processing files
│   │
│   ├── MachineLearning/
│   │   ├── Training/
│   │   │   ├── ML.py           # Model training script
│   │   │   └── phishing_model.joblib
│   │   └── Detection/
│   │       ├── ML.py           # Standalone detection test script
│   │       └── phishing_model.joblib
│   │
│   ├── SimilarFinder/          # Typosquatting detection
│   │   ├── Splitter.py         # Pre-splits domain list alphabetically
│   │   ├── Searcher.py         # Levenshtein-based domain similarity search
│   │   └── a.txt - z.txt       # Pre-split domain corpus files
│   │
│   └── Decryption/             # Standalone decryption utilities
│       ├── Decrypt.py
│       └── Decrypt2.py
│
├── requirements.txt            # Python dependencies
└── install.sh                  # Setup script
```

---

## Installation & Setup

### Python Dependencies

```bash
pip install -r requirements.txt
```

`requirements.txt` includes: `bs4`, `dnspython`, `Levenshtein`, `requests`, `tqdm`, `python-whois`, `urllib3`, `psutil`, `pandas`, `pycryptodome`, `flask`, `scikit-learn`, `joblib`

### Server Setup

```bash
cd Server
npm install
node server.js
```

The server will start on port 4000. Ensure `python3` is available in the system PATH.

### Train the Model (if needed)

```bash
cd Backend/MachineLearning/Training
python ML.py
```

This loads `Backend/Dataset_Files/Shuffled.csv`, trains the Random Forest, and saves `phishing_model.joblib`.

### Build the Dataset from Scratch

```bash
cd Backend/AIO
python aio.py
```

This runs the full pipeline: downloads PhishTank data, cleans it, scrapes features, and outputs a labelled CSV.

### Load the Chrome Extension

1. Open Chrome → `chrome://extensions`
2. Enable **Developer Mode**
3. Click **Load unpacked**
4. Select the `Frontend/` directory

---

## Potential & Roadmap

PhishWarden has a well-defined core that can be significantly extended:

**Short term:**
- **Close the HTTP response loop** — return the Python prediction in the HTTP response body rather than via stdout, so the popup displays the verdict in real time without a polling mechanism.
- **Replace hardcoded AES key** with a server-generated session key or move the server to HTTPS.
- **Add URL bar injection** — instead of only showing the verdict in the popup, inject a visible banner into the page DOM when a phishing site is detected.

**Medium term:**
- **Integrate SimilarFinder into the live pipeline** — after ML classification, if confidence is below a threshold, run a Levenshtein check against known brand domains and combine scores.
- **Retrain on a rolling dataset** — schedule weekly PhishTank downloads and incremental model updates to keep up with evolving phishing vocabulary and techniques.
- **Add URL structure features** — length of domain, count of hyphens, count of digits, presence of brand keywords in the subdomain, number of dots — all of these are strong, computationally free phishing signals currently unused.
- **HTTPS for the server** — deploy with a TLS certificate to make the AES-CBC transport layer redundant for privacy.

**Long term:**
- **Browser-local inference** — convert the Random Forest to ONNX or TensorFlow.js format and run inference directly in the browser's service worker, eliminating the round-trip to the server entirely and enabling offline operation.
- **Federated threat intelligence** — aggregate anonymised signal from all extension users to continuously improve the model without exposing individual browsing data.
- **Screenshot and visual similarity detection** — phishing pages often clone the visual layout of targeted brands. A CNN trained on page screenshots would catch professional phishing attacks that avoid keyword triggers.
- **Multi-classifier ensemble** — combine the Random Forest (tabular features) + SimilarFinder (string similarity) + a visual model (screenshot CNN) into a weighted ensemble verdict for higher precision.
