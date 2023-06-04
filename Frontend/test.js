const headers = new Headers()
headers.append("Content-Type", "application/json")

const body = {
  "test": "event"
}

const options = {
  method: "POST",
  headers,
  mode: "cors",
  body: JSON.stringify(body),
}

fetch("https://eokdhydqf6vxow0.m.pipedream.net", options)
