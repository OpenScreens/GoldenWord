import requests
inputMessage = ["ping","hola",'}e%$>"&/p}']
outputExpected = ["pong","No Pong","No Pong"]

def test_send_message(input,output):
    url = "https://pingpong.test.goldenwordai.com:4998"
    data = {"message": input,"chatid": "123","frontend": "chatpage"}
    response = requests.post(url, json=data)
    assert response.status_code == 200
    print("Test de envío de mensaje exitoso")

def main():
    for i in range(len(inputMessage)):
        test_send_message(inputMessage[i])

if __name__ == "__main__":
    main()
