document.addEventListener("DOMContentLoaded", function () {
    const chatbox = document.getElementById("chatbox");
    const userInput = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");

    // Function to append messages
    function appendMessage(sender, message) {
        const messageElement = document.createElement("div");
        messageElement.className = sender === "user" ? "user-message" : "bot-message";
        messageElement.textContent = message;
        chatbox.appendChild(messageElement);
        chatbox.scrollTop = chatbox.scrollHeight;
    }

    // Function to make the bot speak
    function speak(text) {
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = "en-US"; // You can change this to other languages
        speechSynthesis.speak(utterance);
    }

    // Handle sending a message
    sendBtn.addEventListener("click", function () {
        const userText = userInput.value.trim();
        if (userText === "") return;

        appendMessage("user", userText);
        userInput.value = "";

        // Simulate bot response
        setTimeout(() => {
            let botResponse = "Hello! This is my voice speaking!"; // You can make this dynamic
            appendMessage("bot", botResponse);
            speak(botResponse); // Voice output
        }, 500);
    });

    // Allow pressing Enter to send
    userInput.addEventListener("keypress", function (e) {
        if (e.key === "Enter") {
            sendBtn.click();
        }
    });
});
