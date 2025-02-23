let currentChatUser = "";

function startChat(username) {
    currentChatUser = username;
    document.getElementById("chatWith").innerText = "Chatting with " + username;
    fetchMessages();
}

document.getElementById("sendBtn").addEventListener("click", function() {
    let messageInput = document.getElementById("messageInput").value;
    if (!currentChatUser) {
        alert("Select a user first!");
        return;
    }
    
    fetch("/send_message", {
        method: "POST",
        body: JSON.stringify({ receiver: currentChatUser, message: messageInput }),
        headers: { "Content-Type": "application/json" }
    })
    .then(() => fetchMessages());
    
    document.getElementById("messageInput").value = "";
});

function fetchMessages() {
    if (!currentChatUser) return;

    fetch(`/get_messages/${currentChatUser}`)
    .then(response => response.json())
    .then(messages => {
        let chatBox = document.getElementById("messages");
        chatBox.innerHTML = messages
            .map(msg => `
                <div class="message ${msg.sender === currentChatUser ? 'received' : 'sent'}">
                    <b>${msg.sender === currentChatUser ? currentChatUser : "You"}:</b> ${msg.message}
                </div>
            `)
            .join("");
    });
}

// Fetch messages every 2 seconds
setInterval(fetchMessages, 2000);
