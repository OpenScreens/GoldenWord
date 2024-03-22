import http.client
import json

conn = http.client.HTTPConnection("127.0.0.1", 5000)
payload = json.dumps([
  {
    "message": "¿Cómo estás?",
    "chatid": 1001,
    "frontend": "chatpage"
  },
  {
    "message": "Me gustaría saber más sobre ese tema.",
    "chatid": 1002,
    "frontend": "chatpage"
  },
  {
    "message": "ping",
    "chatid": 1003,
    "frontend": "chatpage"
  },
  {
    "message": "¿Qué planeas hacer?",
    "chatid": 1004,
    "frontend": "chatpage"
  },
  {
    "message": "¿Qué opinas sobre el cambio climático?",
    "chatid": 1005,
    "frontend": "chatpage"
  }
])
headers = {
  'Content-Type': 'application/json'
}
conn.request("POST", "/", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))