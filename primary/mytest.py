import requests

first = requests.get("http://localhost:5001/about")
print(first.json())