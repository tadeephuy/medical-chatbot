import requests

url = 'http://127.0.0.1:5000/proc-nlu'
results = requests.post(
    url, json={'mess': "tao muốn biết thông tin về bệnh thalassemia .",
               '_id': 1})

print(results.json())
