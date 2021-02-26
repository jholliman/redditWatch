import requests

dbsecret = 'Vlrciba3zM5NbVfOnbNQS0F9juEhKMOTkt1Cmh9h'
url = 'https://thewallstreetbots-default-rtdb.firebaseio.com/test/myballs/wednesday.json'
url += '?auth=%s' % (dbsecret)
data = '{"hello": "world"}'

x = requests.post(url, data)
print(x)