import requests
import json

input = {'vote': 'Canada'}
#r = requests.post("http://localhost:5000//api/v1.0/tasks", json = input)
resp = requests.get("http://localhost:5000/fantasy/api/v1.0/predictions")

print (resp.status_code)
print (resp.headers)
print (resp.content)
#print (result["predictions"])
