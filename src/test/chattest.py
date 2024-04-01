import requests

def test_send_message(input,output):
    url = "https://pingpong.test.goldenwordai.com:4998"
    data = {"message": input,"chatid": "123","frontend": "chatpage"}
    response = requests.post(url, json=data)
    assert response.status_code == 200
    print("Test de envío de mensaje exitoso")

def main():
    test_send_message("ping","pong")
    test_send_message("hola","No Pong")
    test_send_message('}e%$>"&/p}"',"No Pong")

if __name__ == "__main__":
    main()
