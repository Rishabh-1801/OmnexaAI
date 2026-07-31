import http from "node:http";
import { readFile, writeFile, mkdir } from "node:fs/promises";
import { existsSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function loadEnv() {
  const envPath = path.join(__dirname, ".env");
  if (!existsSync(envPath)) return;
  const lines = (await readFile(envPath, "utf8")).split(/\r?\n/);
  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#") || !trimmed.includes("=")) continue;
    const [key, ...valueParts] = trimmed.split("=");
    if (!process.env[key]) process.env[key] = valueParts.join("=").trim();
  }
}

await loadEnv();

const port = Number(process.env.PORT || 8787);
const allowedOrigin = process.env.ALLOWED_ORIGIN || "https://www.theomnexaai.com";
const model = process.env.OPENAI_MODEL || "gpt-5.5";
const dataDir = path.join(__dirname, "data");
const publicDir = path.join(__dirname, "public");
const leadsPath = path.join(dataDir, "leads.json");

async function readJson(filePath, fallback) {
  try {
    return JSON.parse(await readFile(filePath, "utf8"));
  } catch {
    return fallback;
  }
}

function sendJson(res, status, data, origin) {
  res.writeHead(status, {
    "Content-Type": "application/json; charset=utf-8",
    "Access-Control-Allow-Origin": origin || allowedOrigin,
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Vary": "Origin"
  });
  res.end(JSON.stringify(data));
}

function sanitizeMessages(messages) {
  if (!Array.isArray(messages)) return [];
  return messages
    .filter((item) => item && ["user", "assistant"].includes(item.role) && typeof item.content === "string")
    .slice(-12)
    .map((item) => ({
      role: item.role,
      content: item.content.slice(0, 1200)
    }));
}

function extractLead(messages) {
  const text = messages.map((message) => message.content).join("\n");
  const email = text.match(/[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}/i)?.[0] || "";
  const phone = text.match(/(?:\+?\d[\d\s().-]{7,}\d)/)?.[0]?.trim() || "";
  if (!email && !phone) return null;

  return {
    email,
    phone,
    transcript: messages,
    createdAt: new Date().toISOString()
  };
}

async function saveLead(lead) {
  await mkdir(dataDir, { recursive: true });
  const existing = await readJson(leadsPath, []);
  existing.push(lead);
  await writeFile(leadsPath, JSON.stringify(existing, null, 2));
}

async function serveStatic(req, res) {
  const url = new URL(req.url, `http://${req.headers.host}`);
  const fileName = url.pathname === "/" ? "demo.html" : url.pathname.replace(/^\/+/, "");
  const filePath = path.join(publicDir, fileName);

  if (!filePath.startsWith(publicDir) || !existsSync(filePath)) {
    res.writeHead(404);
    res.end("Not found");
    return;
  }

  const ext = path.extname(filePath);
  const type = ext === ".js" ? "application/javascript; charset=utf-8" : "text/html; charset=utf-8";
  res.writeHead(200, {
    "Content-Type": type,
    "Cache-Control": "no-store"
  });
  res.end(await readFile(filePath));
}

async function handleChat(req, res) {
  const origin = req.headers.origin || allowedOrigin;
  let body = "";

  req.on("data", (chunk) => {
    body += chunk;
    if (body.length > 12000) req.destroy();
  });

  req.on("end", async () => {
    try {
      if (!process.env.OPENAI_API_KEY) {
        sendJson(res, 500, { error: "OPENAI_API_KEY is missing on the server." }, origin);
        return;
      }

      const payload = JSON.parse(body || "{}");
      const messages = sanitizeMessages(payload.messages);
      if (!messages.length) {
        sendJson(res, 400, { error: "Message is required." }, origin);
        return;
      }

      const knowledge = await readJson(path.join(dataDir, "knowledge.json"), {});
      const lead = extractLead(messages);
      if (lead) await saveLead(lead);

      const instructions = [
        `You are the official website support assistant for ${knowledge.businessName || "The Omnexa AI"}. You work exclusively for this business.`,
        `Tone: ${knowledge.tone || "professional, friendly, concise"}.`,
        "STRICT SCOPE RULE: You must ONLY answer questions that are directly related to the business — including its services, pricing, how it works, FAQs, contact information, and lead capture. This is a non-negotiable rule.",
        "FORBIDDEN: Do NOT answer any general knowledge questions, coding questions, math problems, jokes, news, weather, history, science, or any topic that is not specifically about this business and its services. Even if the visitor insists or rephrases.",
        "When a visitor asks something outside the scope of the business, politely decline and redirect them. Example: 'I'm only able to help with questions about The Omnexa AI and its services. Can I help you with something related to our AI solutions?'",
        "When a visitor seems interested in the services, politely ask for name, email, phone, company, and requirement to connect them with the team.",
        "Never claim a human has been notified unless the visitor has provided their contact details.",
        "Never make up information that is not present in the business knowledge below.",
        `Business knowledge:\n${JSON.stringify(knowledge, null, 2)}`
      ].join("\n\n");

      const response = await fetch("https://api.openai.com/v1/responses", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${process.env.OPENAI_API_KEY}`
        },
        body: JSON.stringify({
          model,
          reasoning: { effort: "low" },
          instructions,
          input: messages
        })
      });

      if (!response.ok) {
        const errorText = await response.text();
        sendJson(res, 502, { error: "AI provider error.", detail: errorText.slice(0, 500) }, origin);
        return;
      }

      const data = await response.json();
      const reply = data.output_text || "Thanks. Please share your name, email, phone number, and requirement so our team can help you.";
      sendJson(res, 200, { reply, leadCaptured: Boolean(lead) }, origin);
    } catch (error) {
      sendJson(res, 500, { error: "Chat failed.", detail: error.message }, origin);
    }
  });
}

const server = http.createServer(async (req, res) => {
  if (req.method === "OPTIONS") {
    sendJson(res, 204, {}, req.headers.origin);
    return;
  }

  if (req.method === "POST" && req.url === "/api/chat") {
    await handleChat(req, res);
    return;
  }

  if (req.method === "GET") {
    await serveStatic(req, res);
    return;
  }

  res.writeHead(405);
  res.end("Method not allowed");
});

server.listen(port, () => {
  console.log(`Omnexa AI chatbot server running at http://localhost:${port}`);
});
