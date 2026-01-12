## 🧱 Tech Stack

**Frontend**

* HTML
* CSS
* JavaScript (Vanilla)

**Backend**

* Python 3.9+
* FastAPI
* Pydantic
* Groq API
* SMTP

---

## 📁 Project Structure

```
email-sender-genai-app/
│
│── backend
│   ├── venv
|   ├──app/
│   │  ├── main.py
│   │  ├── llm.py
│   │  ├── email_service.py
│   │  ├── store.py
│   │  ├── schemas.py
│   │  └── config.py
│   │
|   ├── gui_app.py
|   ├── .env
|   ├── requirements.txt
|
|
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
```

---

## 🛠 Prerequisites (Ubuntu)

* Ubuntu 20.04+
* Python 3.9 or higher
* pip
* Git (optional)

Check Python:

```bash
python3 --version
```

---

## 🚀 Installation & Setup (Ubuntu)

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/ai-cold-email-generator.git
cd ai-cold-email-generator
```

---

### 2️⃣ Create Virtual Environment

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Configure Environment Variables

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key

SMTP_HOST=smtp.gmail.com
SMTP_PORT=465
SMTP_EMAIL=your_email@gmail.com
SMTP_PASSWORD=your_app_password
```

⚠️ Use **Gmail App Password**, not your real password.

---

### 5️⃣ Run Backend Server

```bash
uvicorn app.main:app --reload
```

Backend runs at:

```
http://127.0.0.1:8000
```

---

### 6️⃣ Run Frontend

Open `frontend/index.html` directly in your browser
OR use a simple server:

```bash
cd frontend
python3 -m http.server 8080
```

Open:

```
http://localhost:8080
```

---

## 🔄 How It Works

1. User enters resume + recipient details
2. Frontend sends data to `/generate-email`
3. Groq LLM generates email text
4. Email stored temporarily in memory
5. User clicks **Send**
6. Backend sends email via SMTP

---

## ⚠️ Notes

* Emails are stored **in-memory**, restart clears data
* Not production-ready SMTP setup
* Designed for learning, demos, and portfolios

---

## 📜 License

MIT License
