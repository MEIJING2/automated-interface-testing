import requests
api_url = 'http://localhost:12306/demo1'
reps = requests.get(api_url)
print(reps.text)
print(reps.status_code)
