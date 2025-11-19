let chatOpen = false;

function toggleChat() {
    chatOpen = !chatOpen;
    document.getElementById("chat-body").style.display = chatOpen ? "flex" : "none";
}

function addChatMessage(msg, sender) {
    const div = document.createElement("div");
    div.classList.add(sender === "user" ? "user-msg" : "bot-msg");
    div.textContent = msg;
    document.getElementById("chat-messages").appendChild(div);
    document.getElementById("chat-messages").scrollTop = document.getElementById("chat-messages").scrollHeight;
}

function sendChatMessage() {
    const input = document.getElementById("chat-input");
    const msg = input.value.trim();
    if (!msg) return;
    addChatMessage(msg, "user");
    input.value = "";

    addChatMessage("💬 Bot is typing...", "bot");

    fetch("/chatbot_api", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: msg })
    })
    .then(res => res.json())
    .then(data => {
        const msgs = document.getElementById("chat-messages");
        msgs.removeChild(msgs.lastChild);  // remove typing
        addChatMessage(data.response, "bot");
    })
    .catch(() => {
        const msgs = document.getElementById("chat-messages");
        msgs.removeChild(msgs.lastChild);
        addChatMessage("Oops! Something went wrong.", "bot");
    });
}

document.getElementById("chat-input").addEventListener("keypress", function(e){
    if(e.key === "Enter") sendChatMessage();
});
