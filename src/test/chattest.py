import requests

def test_send_message(input,output):
    url = "https://pingpong.test.goldenwordai.com:4998"
    data = {'response': input, 'chatid': '123'}
    response = requests.post(url, data=data)
    assert response.status_code == 200
    assert response.json() == [{'response': output, 'chatid': '123'}]
    print("Test de envío de mensaje exitoso")

def main():
    test_send_message("ping","pong")
    test_send_message("hola","No Pong")
    test_send_message('}e%$>"&/p}"',"No Pong")

if __name__ == "__main__":
    main()
