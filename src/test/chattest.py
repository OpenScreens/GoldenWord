import json
import requests
inputMessage = ["ping","hola",'}e%$>"&/p}']
outputExpected = ["pong","No Pong","No Pong"]

def test_send_message(input):
    url = "https://pingpong.test.goldenwordai.com:4998"
    data = {"message": input,"chatid": "123","frontend": "chatpage"}
    response = requests.post(url, json=data)
    assert response.status_code == 200
    print(f"Test for sending message '{input}' successful")

def retrieve_server_messages():
    url = "https://pingpong.test.goldenwordai.com:5000/msg"
    response = requests.get(url)
    print(response.json())

def main():
    for i in range(len(inputMessage)):
        test_send_message(inputMessage[i])
        retrieve_server_messages()

if __name__ == "__main__":
    main()
