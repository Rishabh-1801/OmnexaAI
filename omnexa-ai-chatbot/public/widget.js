(function () {
  const currentScript = document.currentScript;
  const apiBase = currentScript?.dataset.apiBase || window.OMNEXA_CHAT_API || "";
  const brand = currentScript?.dataset.brand || "The Omnexa AI";

  const styles = document.createElement("style");
  styles.textContent = `
    .omnexa-chat-root{position:fixed;right:20px;bottom:20px;z-index:999999;font-family:Inter,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:#172033}
    .omnexa-chat-button{width:60px;height:60px;border:0;border-radius:18px;background:#111827;color:#fff;box-shadow:0 18px 45px rgba(17,24,39,.22);cursor:pointer;display:grid;place-items:center}
    .omnexa-chat-button svg{width:28px;height:28px}
    .omnexa-chat-panel{width:min(380px,calc(100vw - 32px));height:560px;max-height:calc(100vh - 110px);background:#fff;border:1px solid #d9e0ea;border-radius:8px;box-shadow:0 24px 70px rgba(15,23,42,.24);display:none;overflow:hidden}
    .omnexa-chat-panel.is-open{display:flex;flex-direction:column}
    .omnexa-chat-header{background:#111827;color:#fff;padding:14px 16px;display:flex;align-items:center;justify-content:space-between;gap:12px}
    .omnexa-chat-title{font-size:15px;font-weight:700;line-height:1.2}
    .omnexa-chat-subtitle{font-size:12px;color:#cbd5e1;margin-top:2px}
    .omnexa-chat-close{border:0;background:transparent;color:#fff;font-size:24px;line-height:1;cursor:pointer}
    .omnexa-chat-messages{flex:1;overflow:auto;padding:14px;background:#f8fafc;display:flex;flex-direction:column;gap:10px}
    .omnexa-chat-msg{max-width:86%;padding:10px 12px;border-radius:8px;font-size:14px;line-height:1.42;white-space:pre-wrap}
    .omnexa-chat-msg.bot{align-self:flex-start;background:#fff;border:1px solid #e2e8f0}
    .omnexa-chat-msg.user{align-self:flex-end;background:#111827;color:#fff}
    .omnexa-chat-lead{display:grid;gap:8px;padding:12px;border-top:1px solid #e2e8f0;background:#fff}
    .omnexa-chat-lead-row{display:grid;grid-template-columns:1fr 1fr;gap:8px}
    .omnexa-chat-input,.omnexa-chat-textarea{width:100%;box-sizing:border-box;border:1px solid #cbd5e1;border-radius:6px;padding:9px 10px;font:inherit;font-size:13px}
    .omnexa-chat-textarea{resize:none;min-height:56px}
    .omnexa-chat-composer{display:flex;gap:8px;padding:12px;border-top:1px solid #e2e8f0;background:#fff}
    .omnexa-chat-composer input{flex:1;border:1px solid #cbd5e1;border-radius:6px;padding:11px 12px;font:inherit;font-size:14px;min-width:0}
    .omnexa-chat-send,.omnexa-chat-lead button{border:0;border-radius:6px;background:#0f766e;color:white;font-weight:700;padding:0 14px;cursor:pointer}
    .omnexa-chat-lead button{height:38px}
    .omnexa-chat-status{font-size:12px;color:#64748b;padding:0 14px 10px;background:#fff;min-height:16px}
    @media(max-width:520px){.omnexa-chat-root{right:12px;bottom:12px}.omnexa-chat-panel{height:calc(100vh - 24px);max-height:none}.omnexa-chat-button{width:56px;height:56px}.omnexa-chat-lead-row{grid-template-columns:1fr}}
  `;
  document.head.appendChild(styles);

  const root = document.createElement("div");
  root.className = "omnexa-chat-root";
  root.innerHTML = `
    <section class="omnexa-chat-panel" aria-label="${brand} chat support">
      <header class="omnexa-chat-header">
        <div>
          <div class="omnexa-chat-title">${brand}</div>
          <div class="omnexa-chat-subtitle">AI support and lead assistant</div>
        </div>
        <button class="omnexa-chat-close" type="button" aria-label="Close chat">&times;</button>
      </header>
      <main class="omnexa-chat-messages"></main>
      <form class="omnexa-chat-lead">
        <div class="omnexa-chat-lead-row">
          <input class="omnexa-chat-input" name="name" placeholder="Name" autocomplete="name">
          <input class="omnexa-chat-input" name="phone" placeholder="Phone" autocomplete="tel">
        </div>
        <input class="omnexa-chat-input" name="email" placeholder="Email" autocomplete="email">
        <textarea class="omnexa-chat-textarea" name="requirement" placeholder="Requirement"></textarea>
        <button type="submit">Send details</button>
      </form>
      <form class="omnexa-chat-composer">
        <input name="message" placeholder="Ask a question..." autocomplete="off">
        <button class="omnexa-chat-send" type="submit">Send</button>
      </form>
      <div class="omnexa-chat-status"></div>
    </section>
    <button class="omnexa-chat-button" type="button" aria-label="Open chat">
      <svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M4 5.5A3.5 3.5 0 0 1 7.5 2h9A3.5 3.5 0 0 1 20 5.5v7A3.5 3.5 0 0 1 16.5 16H10l-5.2 4.4A.5.5 0 0 1 4 20V5.5Z" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><path d="M8 7.5h8M8 11h5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>
    </button>
  `;
  document.body.appendChild(root);

  const panel = root.querySelector(".omnexa-chat-panel");
  const openButton = root.querySelector(".omnexa-chat-button");
  const closeButton = root.querySelector(".omnexa-chat-close");
  const messagesEl = root.querySelector(".omnexa-chat-messages");
  const composer = root.querySelector(".omnexa-chat-composer");
  const leadForm = root.querySelector(".omnexa-chat-lead");
  const status = root.querySelector(".omnexa-chat-status");
  const messages = [
    { role: "assistant", content: "Hi, I can help with services, pricing questions, support, and project enquiries. What would you like to automate with AI?" }
  ];

  function renderMessage(message) {
    const bubble = document.createElement("div");
    bubble.className = `omnexa-chat-msg ${message.role === "user" ? "user" : "bot"}`;
    bubble.textContent = message.content;
    messagesEl.appendChild(bubble);
    messagesEl.scrollTop = messagesEl.scrollHeight;
  }

  function setStatus(text) {
    status.textContent = text || "";
  }

  async function sendToBot(content) {
    messages.push({ role: "user", content });
    renderMessage({ role: "user", content });
    setStatus("Typing...");

    try {
      const response = await fetch(`${apiBase}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ messages })
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.error || "Chat request failed");
      const botMessage = { role: "assistant", content: data.reply };
      messages.push(botMessage);
      renderMessage(botMessage);
      setStatus(data.leadCaptured ? "Details received. Our team can follow up." : "");
    } catch (error) {
      renderMessage({ role: "assistant", content: "Sorry, I could not connect right now. Please try again or share your contact details." });
      setStatus(error.message);
    }
  }

  openButton.addEventListener("click", () => {
    panel.classList.add("is-open");
    openButton.style.display = "none";
    if (messagesEl.childElementCount === 0) renderMessage(messages[0]);
  });

  closeButton.addEventListener("click", () => {
    panel.classList.remove("is-open");
    openButton.style.display = "grid";
  });

  composer.addEventListener("submit", async (event) => {
    event.preventDefault();
    const input = composer.elements.message;
    const content = input.value.trim();
    if (!content) return;
    input.value = "";
    await sendToBot(content);
  });

  leadForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const form = new FormData(leadForm);
    const content = [
      `Name: ${form.get("name") || ""}`,
      `Phone: ${form.get("phone") || ""}`,
      `Email: ${form.get("email") || ""}`,
      `Requirement: ${form.get("requirement") || ""}`
    ].join("\n");
    await sendToBot(content);
    leadForm.reset();
  });
})();
