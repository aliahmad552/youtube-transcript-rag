const sendBtn = document.getElementById("send-btn");
const chatBox = document.getElementById("chat-box");
const youtubeUrl = document.getElementById("youtube-url");
const userQuestion = document.getElementById("user-question");

const API_URL = "http://127.0.0.1:8000/youtube_qa"; // your FastAPI backend URL

sendBtn.addEventListener("click", async () => {
    const url = youtubeUrl.value.trim();
    const question = userQuestion.value.trim();

    if (!url || !question) {
        alert("Please enter both a YouTube URL and your question.");
        return;
    }

    // Add user message to chat
    addMessage(question, "user");

    // Clear input
    userQuestion.value = "";

    // Add typing indicator
    const typingMsg = addMessage("Thinking...", "bot");
    typingMsg.classList.add("typing");

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ url, question }),
        });

        const data = await response.json();

        typingMsg.remove();

        if (response.ok) {
            typeMessage(data.answer, "bot");
        } else {
            addMessage(`⚠️ ${data.detail}`, "bot");
        }
    } catch (error) {
        typingMsg.remove();
        addMessage("❌ Error connecting to the server.", "bot");
    }
});

function addMessage(text, sender) {
    const msgDiv = document.createElement("div");
    msgDiv.classList.add("message", sender);
    msgDiv.textContent = text;
    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
    return msgDiv;
}

function typeMessage(text, sender) {
    const msgDiv = document.createElement("div");
    msgDiv.classList.add("message", sender);
    chatBox.appendChild(msgDiv);

    let i = 0;
    const speed = 25;
    function typing() {
        if (i < text.length) {
            msgDiv.textContent += text.charAt(i);
            i++;
            chatBox.scrollTop = chatBox.scrollHeight;
            setTimeout(typing, speed);
        }
    }
    typing();
}
