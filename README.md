## 📨 AI Cold Email Generator & Sender

## What is this repository for?

This repository contains a **full-stack AI-powered cold email system** that generates and sends personalized professional emails using a Large Language Model (LLM).

The goal of the project is not just to send emails, but to demonstrate how **modern AI-driven backend systems** are designed end-to-end:

* Structured input collection (resume + recipient context)
* Prompt engineering for controlled LLM output
* Stateless API design with temporary state handling
* Separation of concerns across services
* Real-world email delivery via SMTP

This project is ideal for showcasing:

* Backend engineering skills
* AI integration patterns
* System design thinking
* Clean API-driven architecture

---

## What problem does this project solve?

Writing cold emails manually is:

* Time-consuming
* Repetitive
* Hard to personalize at scale

This system:

* Takes structured user input
* Converts it into a well-defined AI prompt
* Generates a concise, professional cold email
* Allows preview before sending
* Sends the email using real SMTP infrastructure

It bridges the gap between **LLMs and production-ready software**.

---

## High-level architecture

The system follows a **clean layered architecture**, where each component has a single responsibility.

```
Frontend (HTML + CSS + JS)
        |
        | HTTP (JSON)
        v
FastAPI Backend
        |
        ├── Prompt Builder
        ├── LLM Service (Groq)
        ├── In-memory Email Store
        └── Email Delivery Service (SMTP)
```

---

## Component breakdown

### 1. Frontend (Client)

* Collects candidate and recipient details
* Sends structured data to the backend
* Displays generated email preview
* Triggers email sending only after user confirmation

Key idea:
**Frontend does not talk to the LLM directly**. All intelligence lives on the backend.

---

### 2. API Layer (FastAPI)

Acts as the orchestration brain.

Responsibilities:

* Input validation using schemas
* Prompt construction
* Calling the LLM service
* Managing generated email lifecycle
* Exposing clean REST endpoints

Endpoints are intentionally simple and explicit:

* Generate email
* Send email

This mirrors how production APIs are designed.

---

### 3. LLM Service (Groq)

* Encapsulates all AI logic
* Uses a strict system prompt to control output
* Ensures:

  * No subject line generation
  * Word limit
  * Professional tone
  * Candidate name inclusion

Key design principle:
**LLM behavior is constrained, not trusted blindly**.

---

### 4. Email Store (Temporary State)

* Stores generated emails using unique IDs
* Decouples generation from sending
* Prevents regeneration during send

This mimics how systems avoid recomputation and maintain consistency without a database.

---

### 5. Email Delivery Service (SMTP)

* Responsible only for sending emails
* Uses environment-based configuration
* Easily replaceable with providers like SES, SendGrid, etc.

Clean separation ensures:

* AI logic ≠ Email infrastructure
* Easy future scaling

---

## Design philosophy

This project intentionally emphasizes:

* **Separation of concerns**
* **Explicit data flow**
* **Stateless APIs with controlled state**
* **Replaceable components**
* **Production-style structure**

Even though the app is small, the architecture scales mentally to much larger systems.

---

## What this project is NOT

* Not a monolithic script
* Not a frontend-only AI demo
* Not tightly coupled to one LLM or one email provider
* Not built for shortcuts

It is designed as a **foundation**, not a toy.

---

## Future goals & roadmap

This repository is meant to evolve into a more advanced system.

Planned directions:

### 🧠 AI & Intelligence

* Agentic workflows (follow-ups, reminders)
* Multi-email sequences
* Tone customization
* Context memory per user

### 📈 Scalability

* Replace in-memory store with Redis / DB
* Async background email sending
* Rate limiting & abuse prevention

### 🖥 Desktop & System Integration

* Electron-based desktop app
* Offline-first UI
* Voice-triggered email generation

### 🔐 Reliability & Observability

* Logging & tracing
* Retry mechanisms
* Failure handling
* Metrics (latency, success rate)

---

## Who is this repo for?

* Backend engineers learning AI integration
* Developers preparing for system design interviews
* Anyone building real GenAI-powered products
* Engineers who want **clarity over magic**

---

## Final note

This repository is less about sending emails
and more about **how to think when building AI systems that survive real-world use**.

## 📦 How to Install

- [Ubuntu Documentation](README-UBUNTU.md)
- [Window Documentation](README-WINDOW.md)
