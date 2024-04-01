function processUserInput() {
	var messageInput = document.getElementById("message-input");
	var message = messageInput.value;
	if (message !== "") {
		appendMessage("sender", message);
		messageInput.value = "";
		sendInputtoServer(message)
		}
	}

function sendInputtoServer(message) {
	const requestOptions = {
		method: "POST",
		body: JSON.stringify
		({
			"message": message,
			"chatid": "1234",
			"frontend": "chatpage"
		}),
		headers: { "Content-Type": "application/json" },
	};

	fetch("https://pingpong.test.goldenwordai.com:5000/array", requestOptions)
		.then((response) => {
			string_response = response.text()
			console.log(string_response);
		})
		.catch((error) => {
			console.error(error);
		});
}

function retrieveServerMessages() {
    const requestOptions = {
        method: "GET",
        redirect: "follow"
    };

    fetch("https://pingpong.test.goldenwordai.com:5000/msg", requestOptions)
		.then(response => response.text())
        .then(raw_response => {
            const responses_array = JSON.parse(raw_response);
            responses_array.forEach(json_response => { 
                const string_response = json_response["response"];
                displayResponse(string_response);
            });
		})
        .catch(error => {
            console.error(error);
            displayResponse("Server /msg error"); 
        });
	}

function displayResponse(message) {
	var chatMessages = document.getElementById("chat-messages");
	appendMessage("receiver", message);
}

function appendMessage(type, message) {
	var chatMessages = document.getElementById("chat-messages");
	var newMessage = document.createElement("div");
	newMessage.classList.add("message", type);
	newMessage.innerHTML = "<p>" + message + "</p>";
	chatMessages.appendChild(newMessage);
	chatMessages.scrollTop = chatMessages.scrollHeight; 
}

function addEnterKeyListener() {
	document.getElementById("message-input").addEventListener("keyup", function(event) {
		if (event.keyCode === 13) {
			event.preventDefault();
			processUserInput();
		}
	});
}

addEnterKeyListener();

document.getElementById("send-button").addEventListener("click", function() {
	processUserInput();
});

setInterval(retrieveServerMessages, 10000);
