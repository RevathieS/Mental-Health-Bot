function appendMessage(sender, message) {
    let chatMessages = document.getElementById("chat-messages");

    let messageElement = document.createElement("p");
    messageElement.classList.add(sender === "bot" ? "bot-message" : "user-message");
    messageElement.textContent = message;

    chatMessages.appendChild(messageElement);

    // Ensure the first message is always visible when scrolling up
    setTimeout(() => {
        chatMessages.scrollTop = 0;
    }, 100);
}

function sendMessage() {
    let userInput = document.getElementById("user-input");
    let userMessage = userInput.value.trim();

    if (userMessage === "") return;

    appendMessage("user", userMessage);

    fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: userMessage })
    })
    .then(response => response.json())
    .then(data => {
        appendMessage("bot", data.response);
    });

    userInput.value = "";
}

function handleKeyPress(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}
