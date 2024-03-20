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
        const myHeaders = new Headers();
        myHeaders.append("Content-Type", "application/json");

        const raw = JSON.stringify({
        "message": 2222
        });

        const requestOptions = {
        method: "POST",
        headers: myHeaders,
        body: raw,
        redirect: "follow"
        };

        fetch("http://127.0.0.1:5000/msg", requestOptions)
        .then((response) => response.text())
        .then((result) => console.log(result))
        .catch((error) => console.error(error));

        
        // if (message.includes("me llamo")) {
        //     var name = message.split("me llamo")[1].trim();
        //     response = "Hola " + capitalizeFirstLetter(name);
        // } else {
        //     message === "ping" ? response = "pong" : message === "pong" ? response = "ping" :   
        //     response = responses[message] || "Lo siento, no entendí. ¿Podrías reformular tu pregunta?";
        // }
     

        
    }
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