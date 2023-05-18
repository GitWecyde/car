from datetime import datetime

import requests

url = 'http://127.0.0.1:5000/location/update'
current_datetime = datetime.now()
datetime_str = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
response = requests.post(url,json={
    "email": "test@gmail.com",
    "marque": "peugeot",
    "start_date": "17/05/2023",
    "end_date": "18/05/2023",
    "prix": "100 €",
    "status" : "En cous de traitement",
    "payment": "en cours de payment"
})

if response.status_code == 200:
    print(response.json())
else:
    print("Error:", response.status_code, response.text)
