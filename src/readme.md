# 🎓 Sākṣin — AI-Powered MOOC Interview Platform

**Sākṣin** is an AI-driven interview system that evaluates MOOC learners in real-time using Large Language Models (LLMs), facial emotion analysis, and structured memory. It simulates a real interview with human-like interactions, evaluates candidate responses, and provides feedback to help learners grow and prepare for real-world technical interviews.

---

## 🚀 Features

### 🎙️ Interactive AI Interviews
- Dynamic, real-time questioning using LLMs (e.g., Gemini, GPT)
- Context-aware follow-up questions
- Long-session memory with Redis

### 🧠 LLM Memory Management
- Uses Redis to store and retrieve previous Q&A
- Maintains conversation context even across disconnects
- Reduces token overload using summarization for long chats

### 📸 Emotion Detection via Webcam
- Captures live video through WebRTC
- Analyzes facial expressions using DeepFace
- Stores emotion states during responses to evaluate confidence

### 📊 Final Evaluation Report
- Auto-evaluation using LLM:
  - Score out of 10
  - Strengths & Weaknesses
  - Category-wise breakdown (Tech, Communication, Confidence)
- Suggestions for improvement
- Stored with session ID for later access

### 📁 Secure Cloud-based Storage
- Interview data stored securely (Redis + PostgreSQL)
- Video & audio can optionally be stored for review (TBD)

---

## 🧱 Tech Stack

| Layer          | Tech                             |
|----------------|----------------------------------|
| Frontend       | Next.js, Tailwind, Framer Motion |
| Backend        | Django + DRF                     |
| Realtime Comm  | WebRTC, WebSockets               |
| LLM Integration| LangChain + Gemini               |
| Memory Store   | Redis                            |
| Emotion Engine | DeepFace                         |
| Database       | PostgreSQL                       |
| Hosting        | Render      |

---

## 🧩 Architecture Overview

```text
                +------------------+
                |   Frontend (Next.js)   |
                +----------+-------+
                           |
        +------------------+------------------+
        | WebRTC Video Feed     | WebSockets Chat |
        |                      |                  |
+---------------+     +----------------+     +-----------------+
|  DeepFace API |<--->| Django + DRF   |<--->| LangChain + LLM |
+---------------+     +----------------+     +-----------------+
                           |
                  +--------+--------+
                  |    Redis Memory  |
                  +-----------------+
