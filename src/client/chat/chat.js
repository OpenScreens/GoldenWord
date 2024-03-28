// var responses = {
//     "hola": "¡Hola! ¿Cómo estás?",
//     "bien vos?" : "Bien!",
//     "bien": "Me alegro de escuchar eso.",
//     "mal": "Espero que te sientas mejor pronto.",
//     "chau" : "¡Adiós! Que tengas un buen día."
// };

function capitalizeFirstLetter(string) {
	return string.charAt(0).toUpperCase() + string.slice(1);
}

function processUserInput() {
	var messageInput = document.getElementById("message-input");
	var message = messageInput.value.trim().toLowerCase(); 
	if (message !== "") {
		appendMessage("sender", message);
		messageInput.value = "";
		var response = "";
		sendInputtoServer(message)
		
		
		// if (message.includes("me llamo")) {
			//     var name = message.split("me llamo")[1].trim();
			//     response = "Hola " + capitalizeFirstLetter(name);
			// } else {
				//     message === "ping" ? response = "pong" : message === "pong" ? response = "ping" :   
				//     response = responses[message] || "Lo siento, no entendí. ¿Podrías reformular tu pregunta?";
				// }
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

	fetch("http://localhost:5000/array", requestOptions)
		.then((response) => response.text())
		.then((data) => {
			console.log(data);
		})
		.catch((error) => {
			console.error(error);
		});
}	
//
function retrieveServerMessages() {
    const requestOptions = {
        method: "GET",
        redirect: "follow"
    };

    fetch("http://localhost:5000/msg", requestOptions)
		.then(response => 
			string_response = response.text()
			const json_response = JSON.parse(data);
			response_message = json_response["response"];
                	displayResponse(response_message);
            });
		})
        .catch(error => {
            console.error(error);
            
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
