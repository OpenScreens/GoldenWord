import json
import requests
inputMessage = ["ping","hola",'}e%$>"&/p}']
outputExpected = ["pong", 'error', 'input was holooa', 'error', 'input was }e%$>"&/p}']
outputr = []

def test_send_message(input):
    url = "https://pingpong.test.goldenwordai.com:4998"
    data = {"message": input,"chatid": "123","frontend": "chatpage"}
    response = requests.post(url, json=data)
    assert response.status_code == 200
    print(f"Test for sending message '{input}' successful")

def retrieve_server_messages():
    url = "https://pingpong.test.goldenwordai.com:5000/msg"
    response = requests.get(url)
    json_data = (response.json())
    for item in json_data:
        message = item.get('response')
        outputr.append(message)

def main():
    for i in range(len(inputMessage)):
        test_send_message(inputMessage[i])
        retrieve_server_messages()
    print("----------------------------")    
    for i in range(len(outputExpected)):
        if outputExpected[i] == outputr[i]:
            print(f"Test '{outputr[i]}' successful")
        else:
            print(f"Test '{outputr[i]} vs {outputExpected[i]}' failed")
if __name__ == "__main__":
    main()
