# The Omnexa AI Website Chatbot

This is a ready starter for an AI chatbot that can answer FAQs, support visitors, and collect leads for `https://www.theomnexaai.com/`.

## Setup

1. Copy `.env.example` to `.env` and add your OpenAI API key.
2. Start the server:

```bash
npm start
```

3. Open:

```text
http://localhost:8787
```

## Add To Website

After deploying this folder to a server such as Render, Railway, VPS, or Vercel-compatible Node hosting, add this before `</body>` on your website:

```html
<script
  src="https://YOUR-CHATBOT-SERVER.com/widget.js"
  data-api-base="https://YOUR-CHATBOT-SERVER.com"
  data-brand="The Omnexa AI">
</script>
```

Keep `OPENAI_API_KEY` only on the server. Do not put it inside website HTML or JavaScript.

## Customize FAQs

Edit `data/knowledge.json` with your real services, pricing notes, support email, business hours, and FAQs. The chatbot uses this as its business knowledge.

## Leads

For this starter, leads are saved in `data/leads.json` when the visitor provides an email or phone number. For production, connect `saveLead()` in `server.js` to your CRM, email tool, Google Sheets, or webhook.

## Notes

- The backend uses OpenAI's Responses API.
- The model is configurable with `OPENAI_MODEL`.
- CORS is restricted with `ALLOWED_ORIGIN`.
