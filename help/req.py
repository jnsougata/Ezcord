import requests

url = 'https://google.com'

data = requests.get(url)

print(data.text)