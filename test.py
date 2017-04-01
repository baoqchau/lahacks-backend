import requests

input = {'vote': 'Canada'}
#r = requests.post("http://localhost:5000//api/v1.0/tasks", json = input)
resp = requests.put("http://localhost:5000/fantasy/api/v1.0/predictions/1", json=input)

print (resp.status_code)
print (resp.headers)
print (resp.content)
