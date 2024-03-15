from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():
    if request.method == 'POST':
        message = request.form.get('message')
        chatid = request.form.get('chatid')
        if message.lower() == "ping":
            print("Pong")
            return f'Pong';
        else:
            return "Error: Mensaje no reconocido"

if __name__ == '__main__':
    app.run(debug=True)
