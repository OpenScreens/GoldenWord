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
 
    // fetch("http://localhost:4998", {
    //     method: "POST",
    //     body: JSON.stringify({
    //       message: userMessage,
    //       frontend: 'chathelp',
    //       user_id:'0000',
    //       chat_id:'0000'

    //     }),
    //     headers: {
    //       "Content-type": "application/json;"
    //     }
    //   })
    //     .then((response) => response.json())
    //     .then((json) => console.log(json));

    setTimeout(() => {
        const responseMessageElement = document.createElement("div");
        responseMessageElement.className = "response-msg";
        responseMessageElement.innerText = "response";
        messageContainer.appendChild(responseMessageElement);
        messageContainer.scrollTop = messageContainer.scrollHeight;
    }, 1000);

    document.getElementById("userMessage").value = "";
    messageContainer.scrollTop = messageContainer.scrollHeight;
}