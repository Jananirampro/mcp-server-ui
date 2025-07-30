const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");

const MCP_SERVER_URL = "https://mcp-server-97hm.onrender.com"; // Replace with your deployed MCP server

function appendMessage(text, sender) {
  const msg = document.createElement("div");
  msg.classList.add("message", sender);
  msg.innerText = text;
  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage() {
  const message = userInput.value.trim();
  if (!message) return;

  appendMessage(message, "user");
  userInput.value = "";

  try {
    const res = await fetch(MCP_SERVER_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ model: "mistralai/mistral-7b-instruct:free", message })
    });

    const data = await res.json();
    appendMessage(data.response || ⚠️ No response", "bot");
  } catch (error) {
    appendMessage("❌ MCP Server error!", "bot");
    console.error(error);
  }
}

sendBtn.addEventListener("click", sendMessage);
userInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") sendMessage();
});
