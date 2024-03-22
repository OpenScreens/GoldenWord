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

function sendMessage() {
	var messageInput = document.getElementById("message-input");
	var message = messageInput.value.trim().toLowerCase(); 
	if (message !== "") {
		appendMessage("sender", message);
		messageInput.value = "";
		var response = "";
		
		// if (message.includes("me llamo")) {
			//     var name = message.split("me llamo")[1].trim();
			//     response = "Hola " + capitalizeFirstLetter(name);
			// } else {
				//     message === "ping" ? response = "pong" : message === "pong" ? response = "ping" :   
				//     response = responses[message] || "Lo siento, no entendí. ¿Podrías reformular tu pregunta?";
				// }
			}
		}
Poll(); 
		
//
function Poll() {
    const requestOptions = {
        method: "GET",
        redirect: "follow"
    };

    fetch("http://127.0.0.1:5000/msg", requestOptions)
		.then(response => response.text()) 
		.then(text => {
			var value = text.split('=')[1].split('&')[0];
			sendResponse(value);
		})
        .catch(error => {
            console.error(error);
            setTimeout(Poll, 10000);
        })
		.finally(() => {
            setTimeout(Poll, 10000);
        });
	}

function sendResponse(message) {
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
			sendMessage();
		}
	});
}

addEnterKeyListener();

document.getElementById("send-button").addEventListener("click", function() {
	sendMessage();
});