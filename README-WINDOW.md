## 📨 AI Cold Email Generator (Windows)

A local AI-powered application to generate and send personalized cold emails using FastAPI and Groq LLM with a simple HTML frontend.

---

## ✨ Features

* AI-written cold emails
* Clean browser-based UI
* FastAPI backend
* Groq LLM
* SMTP email sending
* No database required
* Runs on Windows locally

---

## 🧱 Tech Stack

* Python 3.9+
* FastAPI
* HTML, CSS, JavaScript
* Groq API
* SMTP

---

## 🛠 Prerequisites (Windows)

* Windows 10 / 11
* Python 3.9+
* pip
* Git (optional)

Check Python:

```powershell
python --version
```

---

## 🚀 Installation & Setup (Windows)

### 1️⃣ Clone Repository

```powershell
git clone https://github.com/your-username/ai-cold-email-generator.git
cd ai-cold-email-generator
```

---

### 2️⃣ Create Virtual Environment

```powershell
cd backend
python -m venv venv
venv\Scripts\activate
```

If PowerShell blocks scripts:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

---

### 3️⃣ Install Dependencies

```powershell
pip install -r requirements.txt
```

---

### 4️⃣ Configure `.env` File

Create `.env` in project root:

```env
GROQ_API_KEY=your_groq_api_key

SMTP_HOST=smtp.gmail.com
SMTP_PORT=465
SMTP_EMAIL=your_email@gmail.com
SMTP_PASSWORD=your_app_password
```

---

### 5️⃣ Run Backend

```powershell
uvicorn app.main:app --reload
```

Server runs at:

```
http://127.0.0.1:8000
```

---

### 6️⃣ Run Frontend

Option 1: Double-click `index.html`

Option 2 (recommended):

```powershell
cd frontend
python -m http.server 8080
```

Open browser:

```
http://localhost:8080
```

---

## 🔄 Application Flow

1. Fill resume & recipient form
2. Click **Generate Email**
3. AI creates email using Groq
4. Preview appears
5. Click **Send Email**
6. SMTP sends email

---

## ⚠️ Limitations

* In-memory email storage
* No authentication
* Single-user local setup

---

## 📜 License

MIT License

---
