<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Voice Chatbot</title>
<style>
    body {
        font-family: Arial, sans-serif;
        background: #f4f4f4;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
    }
    #chat-container {
        width: 400px;
        background: white;
        border-radius: 8px;
        box-shadow: 0px 0px 10px rgba(0,0,0,0.2);
        display: flex;
        flex-direction: column;
    }
    #chatbox {
        flex: 1;
        padding: 10px;
        overflow-y: auto;
        border-bottom: 1px solid #ccc;
    }
    .user {
        text-align: right;
        margin: 5px 0;
        color: blue;
    }
    .bot {
        text-align: left;
        margin: 5px 0;
        color: green;
    }
    #input-area {
        display: flex;
    }
    #user-input {
        flex: 1;
        padding: 10px;
        border: none;
        outline: none;
    }
    #send-btn {
        padding: 10px;
        background: #007bff;
        color: white;
        border: none;
        cursor: pointer;
    }
</style>
</head>
<body>

<div id="chat-container">
    <div id="chatbox"></div>
    <div id="input-area">
        <input type="text" id="user-input" placeholder="Type a message...">
        <button id="send-btn">Send</button>
    </div>
</div>

<script>
    const chatbox = document.getElementById("chatbox");
    const userInput = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");

    function displayMessage(message, sender) {
        let msgDiv = document.createElement("div");
        msgDiv.className = sender;
        msgDiv.textContent = message;
        chatbox.appendChild(msgDiv);
        chatbox.scrollTop = chatbox.scrollHeight;
    }

    function speakText(text) {
        let utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = "en-US"; // Change to "hi-IN", "kn-IN", etc.
        speechSynthesis.speak(utterance);
    }

    sendBtn.addEventListener("click", () => {
        let text = userInput.value.trim();
        if (text === "") return;

        // User message
        displayMessage(text, "user");
        userInput.value = "";

        // Bot response (replace with your chatbot logic)
        let botReply = "You said: " + text;
        
        // Show and speak bot reply
        displayMessage(botReply, "bot");
        speakText(botReply);
    });

    // Allow Enter key to send message
    userInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") {
            sendBtn.click();
        }
    });
</script>

</body>
</html>
