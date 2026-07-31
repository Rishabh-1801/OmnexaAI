(function () {
  const currentScript = document.currentScript;
  const apiBase = currentScript?.dataset.apiBase || window.OMNEXA_CHAT_API || "";
  const brand = currentScript?.dataset.brand || "OMNEXA AI Assistant";

  const styles = document.createElement("style");
  styles.textContent = `
    /* ── Base Variables ── */
    .omnexa-chat-root {
      --omn-primary: #111827;
      --omn-accent: #0f766e;
      --omn-radius: 16px;
      --omn-shadow: 0 24px 70px rgba(15,23,42,.28);
      position: fixed;
      right: 20px;
      bottom: 20px;
      z-index: 999999;
      font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color: #172033;
    }

    /* ── Toggle Button ── */
    .omnexa-chat-button {
      width: 60px;
      height: 60px;
      border: 0;
      border-radius: 18px;
      background: var(--omn-primary);
      color: #fff;
      box-shadow: 0 18px 45px rgba(17,24,39,.28);
      cursor: pointer;
      display: grid;
      place-items: center;
      transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .omnexa-chat-button:hover {
      transform: scale(1.07);
      box-shadow: 0 22px 55px rgba(17,24,39,.35);
    }
    .omnexa-chat-button svg { width: 28px; height: 28px; }

    /* ── Panel ── */
    .omnexa-chat-panel {
      width: min(380px, calc(100vw - 32px));
      height: 560px;
      max-height: calc(100vh - 110px);
      background: #fff;
      border: 1px solid #d9e0ea;
      border-radius: var(--omn-radius);
      box-shadow: var(--omn-shadow);
      display: none;
      overflow: hidden;
      transition: opacity 0.2s ease, transform 0.2s ease;
    }
    .omnexa-chat-panel.is-open {
      display: flex;
      flex-direction: column;
    }

    /* ── Header ── */
    .omnexa-chat-header {
      background: var(--omn-primary);
      color: #fff;
      padding: 14px 16px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      flex-shrink: 0;
    }
    .omnexa-chat-header-info { display: flex; align-items: center; gap: 10px; }
    .omnexa-chat-avatar {
      width: 36px; height: 36px;
      border-radius: 10px;
      background: #1f2937;
      display: grid; place-items: center;
      flex-shrink: 0;
    }
    .omnexa-chat-avatar svg { width: 20px; height: 20px; }
    .omnexa-chat-title { font-size: 14px; font-weight: 700; line-height: 1.2; }
    .omnexa-chat-subtitle { font-size: 11px; color: #6ee7b7; margin-top: 2px; display: flex; align-items: center; gap: 5px; }
    .omnexa-online-dot { width: 7px; height: 7px; border-radius: 50%; background: #34d399; display: inline-block; }
    .omnexa-chat-close {
      border: 0;
      background: rgba(255,255,255,0.1);
      color: #fff;
      font-size: 18px;
      line-height: 1;
      cursor: pointer;
      width: 32px; height: 32px;
      border-radius: 8px;
      display: grid; place-items: center;
      flex-shrink: 0;
      transition: background 0.2s;
    }
    .omnexa-chat-close:hover { background: rgba(255,255,255,0.2); }

    /* ── Messages ── */
    .omnexa-chat-messages {
      flex: 1;
      overflow-y: auto;
      overflow-x: hidden;
      padding: 14px;
      background: #f8fafc;
      display: flex;
      flex-direction: column;
      gap: 10px;
      -webkit-overflow-scrolling: touch;
    }
    .omnexa-chat-msg {
      max-width: 86%;
      padding: 10px 13px;
      border-radius: 12px;
      font-size: 14px;
      line-height: 1.5;
      white-space: pre-wrap;
      word-break: break-word;
    }
    .omnexa-chat-msg.bot {
      align-self: flex-start;
      background: #fff;
      border: 1px solid #e2e8f0;
      border-bottom-left-radius: 4px;
    }
    .omnexa-chat-msg.user {
      align-self: flex-end;
      background: var(--omn-primary);
      color: #fff;
      border-bottom-right-radius: 4px;
    }

    /* ── Lead Form ── */
    .omnexa-chat-lead {
      display: grid;
      gap: 8px;
      padding: 12px;
      border-top: 1px solid #e2e8f0;
      background: #fff;
      flex-shrink: 0;
    }
    .omnexa-chat-lead-row { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
    .omnexa-chat-input, .omnexa-chat-textarea {
      width: 100%;
      box-sizing: border-box;
      border: 1px solid #cbd5e1;
      border-radius: 8px;
      padding: 9px 10px;
      font: inherit;
      font-size: 13px;
      outline: none;
      transition: border-color 0.2s;
    }
    .omnexa-chat-input:focus, .omnexa-chat-textarea:focus { border-color: var(--omn-accent); }
    .omnexa-chat-textarea { resize: none; min-height: 56px; }

    /* ── Composer ── */
    .omnexa-chat-composer {
      display: flex;
      gap: 8px;
      padding: 10px 12px;
      border-top: 1px solid #e2e8f0;
      background: #fff;
      flex-shrink: 0;
      padding-bottom: max(10px, env(safe-area-inset-bottom));
    }
    .omnexa-chat-composer input {
      flex: 1;
      border: 1px solid #cbd5e1;
      border-radius: 8px;
      padding: 11px 12px;
      font: inherit;
      font-size: 14px;
      min-width: 0;
      outline: none;
      transition: border-color 0.2s;
    }
    .omnexa-chat-composer input:focus { border-color: var(--omn-accent); }
    .omnexa-chat-send, .omnexa-chat-lead button {
      border: 0;
      border-radius: 8px;
      background: var(--omn-accent);
      color: white;
      font-weight: 700;
      font-size: 14px;
      padding: 0 16px;
      cursor: pointer;
      transition: background 0.2s;
      white-space: nowrap;
    }
    .omnexa-chat-send:hover, .omnexa-chat-lead button:hover { background: #0d6b63; }
    .omnexa-chat-lead button { height: 40px; width: 100%; }

    /* ── Status ── */
    .omnexa-chat-status {
      font-size: 12px;
      color: #64748b;
      padding: 0 14px 8px;
      background: #fff;
      min-height: 14px;
      flex-shrink: 0;
    }

    /* ════════════════════════════════════════
       MOBILE RESPONSIVE  (≤ 600px)
       Chat panel = full-screen overlay
    ════════════════════════════════════════ */
    @media (max-width: 600px) {
      .omnexa-chat-root {
        right: 0;
        bottom: 0;
        left: 0;
        top: 0;
        pointer-events: none;
      }
      /* Keep toggle button in bottom-right corner */
      .omnexa-chat-button {
        pointer-events: all;
        position: absolute;
        right: 16px;
        bottom: 16px;
        width: 56px;
        height: 56px;
        border-radius: 16px;
      }
      /* Full-screen panel */
      .omnexa-chat-panel {
        pointer-events: all;
        position: absolute;
        inset: 0;
        width: 100%;
        height: 100%;
        max-height: 100%;
        border-radius: 0;
        border: none;
        box-shadow: none;
      }
      /* Safe area for notch/home bar */
      .omnexa-chat-header {
        padding-top: max(14px, env(safe-area-inset-top));
        padding-left: max(16px, env(safe-area-inset-left));
        padding-right: max(16px, env(safe-area-inset-right));
      }
      .omnexa-chat-composer {
        padding-bottom: max(12px, env(safe-area-inset-bottom));
      }
      /* Bigger touch targets on mobile */
      .omnexa-chat-composer input { font-size: 16px; padding: 13px 12px; }
      .omnexa-chat-send { height: 48px; padding: 0 18px; font-size: 15px; }
      .omnexa-chat-msg { font-size: 14px; max-width: 90%; }
      .omnexa-chat-lead-row { grid-template-columns: 1fr; }
      .omnexa-chat-input { font-size: 16px; padding: 11px 12px; }
      .omnexa-chat-textarea { font-size: 16px; }
      .omnexa-chat-close { width: 36px; height: 36px; font-size: 20px; }
    }
  `;
  document.head.appendChild(styles);

  const root = document.createElement("div");
  root.className = "omnexa-chat-root";
  root.innerHTML = `
    <section class="omnexa-chat-panel" aria-label="${brand} chat support">
      <header class="omnexa-chat-header">
        <div class="omnexa-chat-header-info">
          <div class="omnexa-chat-avatar">
            <svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M4 5.5A3.5 3.5 0 0 1 7.5 2h9A3.5 3.5 0 0 1 20 5.5v7A3.5 3.5 0 0 1 16.5 16H10l-5.2 4.4A.5.5 0 0 1 4 20V5.5Z" stroke="#6ee7b7" stroke-width="1.8" stroke-linejoin="round"/><path d="M8 7.5h8M8 11h5" stroke="#6ee7b7" stroke-width="1.8" stroke-linecap="round"/></svg>
          </div>
          <div>
            <div class="omnexa-chat-title">${brand}</div>
            <div class="omnexa-chat-subtitle"><span class="omnexa-online-dot"></span>Online &bull; Ready to help</div>
          </div>
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
        <input name="message" placeholder="Type your message..." autocomplete="off">
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

  function isMobile() { return window.matchMedia("(max-width: 600px)").matches; }

  openButton.addEventListener("click", () => {
    panel.classList.add("is-open");
    openButton.style.display = "none";
    if (isMobile()) document.body.style.overflow = "hidden";
    if (messagesEl.childElementCount === 0) renderMessage(messages[0]);
    // Focus composer input for quick typing
    setTimeout(() => composer.elements.message && composer.elements.message.focus(), 150);
  });

  closeButton.addEventListener("click", () => {
    panel.classList.remove("is-open");
    openButton.style.display = "grid";
    document.body.style.overflow = "";
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
