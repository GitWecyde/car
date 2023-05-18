from _datetime import datetime

import requests

url = 'http://127.0.0.1:5000/location/delete/test@gmail.com'

response = requests.get(url)

if response.status_code == 200:
    print(response.json())
else:
    print("Error:", response.status_code, response.text)
