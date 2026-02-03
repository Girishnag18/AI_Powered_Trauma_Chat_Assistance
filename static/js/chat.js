function sendMessage() {
  const input = document.getElementById("msg");
  const msg = input.value.trim();
  if (!msg) return;

  const chatBox = document.getElementById("chatBox");

  // Show user message
  chatBox.innerHTML += `
    <div class="chat-bubble chat-user">${msg}</div>
  `;
  chatBox.scrollTop = chatBox.scrollHeight;

  input.value = "";

  const csrfToken = document
    .querySelector('meta[name="csrf-token"]')
    .getAttribute("content");

  fetch("/chat/send", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken
    },
    body: JSON.stringify({ message: msg })
  })
  .then(res => res.json())
  .then(data => {
    chatBox.innerHTML += `
      <div class="chat-bubble chat-ai">${data.reply}</div>
    `;
    chatBox.scrollTop = chatBox.scrollHeight;

    // Support panel logic
    const panel = document.getElementById("alertBox");
    if (data.severity === "High" || data.severity === "Critical") {
      panel.classList.remove("hidden");
      panel.innerHTML = `
        <h3>⚠ Immediate Support Recommended</h3>
        <p>Your responses suggest elevated distress.</p>
        <p><strong>India Mental Health Helpline:</strong> 9152987821</p>
        <a href="/admin" class="btn btn-primary" style="margin-top:10px;">
          Consult Doctor
        </a>
      `;
    }
  });
}
