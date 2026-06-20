# 🤖 JARVIS Email Console — Smart Email Assistant

A Streamlit-based AI email assistant with a cyberpunk JARVIS-style interface. It connects to your Gmail inbox, pulls your latest unread emails, and uses Google's Gemini AI to analyze and brief you on them — flagging anything urgent (exams, hall tickets, lab tests, official notices, account lockouts) and pushing an instant WhatsApp alert when it does.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit)
![Gemini](https://img.shields.io/badge/AI-Gemini-8E75B2?logo=google)
![Status](https://img.shields.io/badge/Status-Active-success)

---

## ✨ Features

- 📥 **Inbox Scan** — Connects securely to Gmail via IMAP and fetches your latest unread emails.
- 🧠 **AI Intelligence Briefing** — Gemini reads each email and generates a JARVIS-style summary, action assessment, and draft reply suggestion.
- 🚨 **Critical Detection** — Automatically classifies emails as `CRITICAL` or `NORMAL` (exam schedules, hall tickets, lab tests, university notices, account lockouts, urgent action items).
- 📲 **Instant WhatsApp Alerts** — Critical emails trigger an automatic WhatsApp notification via `pywhatkit`.
- 🛡️ **Retry Protocol** — Built-in retry logic to gracefully handle Gemini API rate limits / `503` errors.
- 🎨 **Cyberpunk Glassmorphism UI** — Custom CSS injects a frosted-glass, neon-accented JARVIS console aesthetic into the Streamlit interface.

---

## 🖥️ Tech Stack

| Layer | Technology |
|---|---|
| UI / Frontend | [Streamlit](https://streamlit.io/) |
| AI Engine | Google Gemini (`google-genai`) |
| Email Access | `imaplib`, `email` (Gmail IMAP) |
| Notifications | `pywhatkit` (WhatsApp Web automation) |
| Config | `python-dotenv` |

---

## 📂 Project Structure

```
SmartEmailAssistant/
├── app.py          # Main Streamlit application
├── .gitignore
└── .env            # Your local environment variables (not committed)
```

---

## ⚙️ Setup & Installation

### 1. Clone the repo
```bash
git clone https://github.com/Shabazshiek/SmartEmailAssistant.git
cd SmartEmailAssistant
```

### 2. Install dependencies
```bash
pip install streamlit python-dotenv google-genai pywhatkit
```

> 💡 Tip: Run `pip freeze > requirements.txt` once your environment works, so others can `pip install -r requirements.txt`.

### 3. Configure environment variables
Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_gmail_app_password
PHONE_NUMBER=+91XXXXXXXXXX
```

**Important:**
- `EMAIL_PASS` must be a [Gmail App Password](https://myaccount.google.com/apppasswords), not your regular account password (requires 2FA enabled on your Google account).
- `PHONE_NUMBER` must be in international format and logged into WhatsApp Web in your default browser for `pywhatkit` to work.
- Get a `GEMINI_API_KEY` from [Google AI Studio](https://aistudio.google.com/).

### 4. Run the app
```bash
streamlit run app.py
```

---

## 🚀 Usage

1. Launch the app — you'll land on the **JARVIS // Personal Email Console** dashboard.
2. Click **🔄 Initialize Inbox Scan** in the sidebar.
3. JARVIS fetches your 3 most recent emails and analyzes each one with Gemini.
4. For every email you get:
   - **Intelligence Briefing** — a sharp summary of the content
   - **Action Assessment** — what to do about it (or a witty dismissal if it's junk)
   - **Draft Protocol** — a suggested reply template, if relevant
5. If an email is flagged `CRITICAL`, you'll automatically receive a WhatsApp alert summarizing it.

---

## ⚠️ Notes & Limitations

- Currently fetches only the **latest 3 emails** from the inbox (not strictly unread-only — uses `ALL` search).
- WhatsApp alerts rely on `pywhatkit` opening WhatsApp Web in a browser tab, so a logged-in session is required.
- Gemini model used: `gemini-3.5-flash` — update the model string in `app.py` if it changes or is deprecated.
- Credentials are loaded from `.env` — never commit this file. Make sure it's listed in `.gitignore`.

---

## 🛣️ Roadmap Ideas

- [ ] Add a `requirements.txt`
- [ ] Filter for genuinely unread emails (`UNSEEN` IMAP flag) instead of last 3
- [ ] Add auto-reply / send-draft functionality directly from the UI
- [ ] Support multiple email providers (Outlook, Yahoo) beyond Gmail
- [ ] Persist scan history / logs

---

## 👤 Author

**Shabaz (Stark)**
- GitHub: [@Shabazshiek](https://github.com/Shabazshiek)
- LinkedIn: [sharfuddin-shaik](https://linkedin.com/in/sharfuddin-shaik/)

---

## 📄 License

This project currently has no license specified. Consider adding an [MIT License](https://choosealicense.com/licenses/mit/) if you intend others to use or contribute to it.
