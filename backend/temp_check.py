import time, requests

time.sleep(3)
resp = requests.get('http://localhost:8000/api/health/')
print('status', resp.status_code)
print(resp.text)
