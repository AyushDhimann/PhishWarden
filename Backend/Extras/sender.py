import requests

url = 'http://pawbox.me:4000/api'
headers = {'Content-Type': 'application/json'}
data = {'name': 'John', 'age': 30}

response = requests.post(url, headers=headers, json=data)

if response.status_code == 200:
    print('Success!')
else:
    print('Error:', response.status_code)
