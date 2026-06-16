# WhatsApp-Based Leave Application Agent 🤖📱

An AI-powered Leave Management System that automates employee leave requests through WhatsApp.

Employees can send leave requests in natural language (e.g., *"Hi, I need 2 days sick leave because of fever"*) and the system will:

* Understand the leave request using an LLM (Google Gemini)
* Extract leave details automatically
* Check leave balance
* Approve or reject based on leave policy
* Update Google Sheets automatically
* Reply back to employees on WhatsApp instantly

---

## 🚀 Features

* **WhatsApp Integration** using Twilio Sandbox
* **AI-based Leave Extraction** using Google Gemini API
* **Leave Approval Logic**
* **Google Sheets Database**
* **Real-time Webhook Processing**
* **Automatic WhatsApp Replies**
* **No HR intervention required for routine leave requests**

---

## 🛠 Tech Stack

* Python
* FastAPI
* Twilio WhatsApp API
* Google Gemini API
* Google Sheets API
* ngrok
* Google Colab

---

---

## I Have Created This In Google Collab So I Have Upload A Single File Named Automated Whatsapp leave Bots

---

---

## 📂 Project Structure

```bash
.
├── app.py                 # Main FastAPI server
├── leave_logic.py         # Leave approval logic
├── llm_extractor.py       # Gemini AI leave extraction
├── sheets.py              # Google Sheets integration
├── requirements.txt       # Dependencies
├── credentials.json       # Google service account credentials
└── README.md
```

---

## ⚙️ Setup Guide

### 1. Clone Repository

```bash
git clone https://github.com/Devraj0603/whatsapp-leave-agent.git
cd whatsapp-leave-agent
```

---

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Setup APIs

### Twilio Setup

1. Create account at Twilio
2. Activate WhatsApp Sandbox
3. Join Sandbox from your WhatsApp
4. Copy Sandbox Number

---

### Google Gemini API

1. Open Google AI Studio
2. Generate API key
3. Add API key in code

Example:

```python
genai.configure(api_key="YOUR_GEMINI_API_KEY")
```
### Or You Can Use OpenRouter For Free LLM Use
---

### Google Sheets Setup

1. Create a Google Cloud Project
2. Enable:

   * Google Sheets API
   * Google Drive API
3. Create Service Account
4. Download `credentials.json`
5. Share your Google Sheet with the service account email

---

## 📊 Google Sheet Format

### Sheet 1: Leave Records

| Employee | Leave Type | Days | Reason | Status |
| -------- | ---------- | ---- | ------ | ------ |

---

### Sheet 2: Leave Balances

| Employee | Sick | Casual |
| -------- | ---- | ------ |
| Raj      | 5    | 3      |
| Priya    | 2    | 1      |

---

## ▶ Running the Project

### Start FastAPI Server

```bash
uvicorn app:app --reload
```

---

### Start ngrok

```bash
ngrok http 8000
```

Copy generated URL:

```bash
https://xxxx.ngrok-free.app
```

---

### Configure Twilio Webhook

Set webhook URL:

```bash
https://xxxx.ngrok-free.app/whatsapp
```

Method:

```bash
POST
```

---

## 💬 Example Flow

Employee sends on WhatsApp:

```text
Hi this is Raj.
I need 2 days sick leave because of fever.
```

AI extracts:

```json
{
  "employee": "Raj",
  "leave_type": "sick",
  "days": 2,
  "reason": "fever"
}
```

System checks leave balance:

```text
Raj Sick Leave Available: 5
Requested: 2
```

Approved.

Google Sheet updates:

| Raj | sick | 2 | fever | Approved |

WhatsApp reply:

```text
Leave Approved
Employee: Raj
Type: sick
Days: 2
Remaining Balance: 3
```

---

## 🔄 Workflow

```text
WhatsApp Message
      ↓
Twilio Webhook
      ↓
FastAPI Server
      ↓
Gemini AI
      ↓
Leave Extraction
      ↓
Check Leave Balance
      ↓
Update Google Sheets
      ↓
Send WhatsApp Reply
```

---

## 🎯 Future Improvements

* Admin Dashboard
* Employee Authentication
* Leave History Tracking
* Email Notifications
* Monthly Reports
* Multiple Leave Types
* Deployment on Render

---

## 📌 Use Cases

* HR Automation
* Employee Leave Management
* Small Businesses
* Startups
* Internal Office Automation

---

## 👨‍💻 Author

Developed by **Devraj Gupta**

---

## 📄 License

This project is open-source and available under the MIT License.
