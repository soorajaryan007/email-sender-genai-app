## 📨 AI Email Sender

**(Vue + FastAPI + Electron + Docker)**

A professional **AI-powered email generator and sender** that helps create and send cold emails effortlessly.

The project supports **two ways to run**:

* 🖥️ **Desktop App** using **Electron**
* 🐳 **One-command Browser App** using **Docker** (recommended for easy sharing)

Built with **Vue 3** for UI, **FastAPI** for backend, and **Groq LLM** for AI email generation.

---

## ✨ Features

* 🧠 AI-generated professional cold emails (Groq LLM)
* 📧 Send emails via SMTP (Gmail, Outlook, custom domains)
* 🎨 Modern Vue 3 UI
* ⚙️ FastAPI backend with validation
* 🖥️ Native desktop app (Electron)
* 🌐 Browser-based app (Docker)
* 🐳 One-command startup with Docker
* 🔒 Secure handling of API keys & credentials
* 💻 Cross-platform (Windows, Linux, macOS)

---

## 🧱 Tech Stack

### Frontend

* Vue 3
* Vite
* Axios
* NGINX (Docker production serving)

### Backend

* FastAPI
* Pydantic
* Groq LLM API
* SMTP (email sending)

### Desktop

* Electron

### Infrastructure

* Docker
* Docker Compose

---

## 🧠 Architecture Overview

### Docker / Browser Mode

```
Browser
 └── http://localhost:8080
       └── Vue UI (NGINX, Docker)
             └── FastAPI Backend (Docker)
                   └── Groq LLM + SMTP
```

### Electron / Desktop Mode

```
Electron App
 └── Vue (Vite build)
       └── FastAPI (localhost:8000)
             └── Groq LLM + SMTP
```

---

## 📂 Project Structure

```
project/
│
├── backend/
│   ├── app/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env                # NOT committed
│
├── frontend/
│   ├── src/
│   ├── dist/               # Vue production build
│   ├── Dockerfile
│   └── vite.config.js
│
├── desktop/                # Electron app
│   ├── main.js
│   └── preload.js
│
├── docker-compose.yml
├── start.sh                # Linux / macOS
├── start.bat               # Windows
├── .gitignore
└── README.md
```

---

# 🐳 RUN USING DOCKER (RECOMMENDED)

This is the **easiest way**, especially for **non-technical users**.

---

## 🛠️ Prerequisites (One-Time)

* **Docker Desktop**

Download:
👉 [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)

Supported OS:

* Windows 10 / 11 (64-bit)
* Linux
* macOS

> ❗ No Python, Node.js, or npm required when using Docker.

---

## 🔐 Environment Variables Setup

Create this file:

```
backend/.env
```

Add:

```env
GROQ_API_KEY=
SMTP_HOST=
SMTP_PORT=
SMTP_EMAIL=
SMTP_PASSWORD=
```

---

### 🔑 How to get values

#### Groq API Key

👉 [https://console.groq.com/keys](https://console.groq.com/keys)
(Create an account → Create API Key)

Example:

```env
GROQ_API_KEY=gsk_xxxxxxxxxxxxx
```

---

#### Gmail SMTP (Recommended)

1. Enable 2-Step Verification
   👉 [https://myaccount.google.com/security](https://myaccount.google.com/security)

2. Create App Password
   👉 [https://myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)

   * App: Mail
   * Device: Other

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=465
SMTP_EMAIL=yourgmail@gmail.com
SMTP_PASSWORD=your_app_password
```

---

## 🚀 Start the App (One Command)

### Option 1️⃣: Docker Compose

```bash
docker compose up
```

Open browser:

```
http://localhost:8080
```

---

### Option 2️⃣: One-Click Script (Recommended)

#### 🐧 Linux / macOS

```bash
chmod +x start.sh
./start.sh
```

#### 🪟 Windows

Double-click:

```
start.bat
```

Then open:

```
http://localhost:8080
```

---

## 🧑‍🤝‍🧑 For Non-Technical Users (Docker Mode)

```
1. Install Docker Desktop
2. Open project folder
3. Double-click start.sh (Linux/macOS) or start.bat (Windows)
4. Open browser → http://localhost:8080
```

That’s it.

---

# 🖥️ RUN AS DESKTOP APP (ELECTRON)

Use this if you want a **native desktop application**.

---

## 🛠️ Prerequisites (Electron Mode)

* Node.js ≥ 18
* npm ≥ 9
* Python ≥ 3.10

---

## 🚀 Electron Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/<repo-name>.git
cd <repo-name>
```

---

### 2️⃣ Backend setup

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend runs at:

```
http://localhost:8000
```

---

### 3️⃣ Frontend build

```bash
cd ../frontend
npm install
npm run build
```

---

### 4️⃣ Run Electron

```bash
cd ../desktop
npm install
npm run electron
```

🎉 Desktop app launches.

---

## ⚠️ Important Notes

* ❌ Never commit `.env`
* ❌ Never share API keys
* ✅ Each user should use their own email credentials
* Docker mode is easiest for sharing
* Electron mode is best for desktop distribution

---

## 🔄 Electron vs Docker

| Use Case            | Best Option |
| ------------------- | ----------- |
| Non-technical users | Docker      |
| One-click startup   | Docker      |
| Desktop app feel    | Electron    |
| Portfolio demo      | Either      |
| SaaS / Cloud future | Docker      |

---

## 🚀 Future Improvements

* Single-port setup (remove CORS completely)
* Docker Hub image (no local build)
* Save email history
* User authentication
* Auto-start backend in Electron
* One-click installer (`.exe`, `.AppImage`)
* Cloud deployment

---

## 🏆 Why this project matters

This project demonstrates:

* Full-stack engineering
* Dockerized production architecture
* Desktop + browser delivery
* Secure secret handling
* Real-world API design

Perfect for **portfolio**, **interviews**, and **internal tools**.

---

## 📜 License

MIT License

---

# email-sender-genai-app
