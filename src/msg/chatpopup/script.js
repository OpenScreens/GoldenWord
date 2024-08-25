function openForm() {
    document.getElementById("myForm").style.display = "block";
}

function closeForm() {
    document.getElementById("myForm").style.display = "none";
}

function sendMessage(event) {
    event.preventDefault();
    const messageContainer = document.getElementById("messageContainer");
    const userMessage = document.getElementById("userMessage").value;

    const userMessageElement = document.createElement("div");
    userMessageElement.className = "user-msg";
    userMessageElement.innerText = userMessage;
    messageContainer.appendChild(userMessageElement);
 
    fetch("http://localhost:5000/", {
        method: "POST",
        body: JSON.stringify({
          user_input: userMessage,
        }),
        headers: {
          "Content-type": "application/json"
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(json => {
        const responseMessageElement = document.createElement("div");
        responseMessageElement.className = "response-msg";
        responseMessageElement.innerText = json.response;
        messageContainer.appendChild(responseMessageElement);
        messageContainer.scrollTop = messageContainer.scrollHeight;
    })
    .catch((error) => {
        console.error('Error:', error);
        const errorMessageElement = document.createElement("div");
        errorMessageElement.className = "error-msg";
        errorMessageElement.innerText = "An error occurred while sending the message. Please try again.";
        messageContainer.appendChild(errorMessageElement);
        messageContainer.scrollTop = messageContainer.scrollHeight;
    });

    document.getElementById("userMessage").value = "";
    messageContainer.scrollTop = messageContainer.scrollHeight;
}