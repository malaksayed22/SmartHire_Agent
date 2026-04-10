# 🤖 SmartHire — AI Recruitment Agent

![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.135-green)
![Groq](https://img.shields.io/badge/AI-Groq%20LLaMA-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

> AI-powered recruitment agent that automatically reads resumes, scores candidates, ranks applicants, and answers job-related questions — built with FastAPI and Groq AI.

---

## 📑 Table of Contents

### 📌 Overview
- [📖 About the Project](#about-the-project)
- [✨ Features](#features)
- [🛠 Tech Stack](#tech-stack)

### 🏗 Architecture & Design
- [📂 Project Structure](#project-structure)
- [⚙️ How It Works](#how-it-works)

### 🚀 Usage
- [▶️ Getting Started](#getting-started)
- [🔌 API Endpoints](#api-endpoints)

### 👥 Team & Contribution
- [🤝 Team](#team)

---

## 📖 About the Project

SmartHire is a web-based HR recruitment system that uses AI and automation to make hiring faster and easier. This repository contains the **AI Agent** component of the system.

Instead of HR staff manually reading every resume, the SmartHire agent:
- Automatically reads and understands resumes (PDF or DOCX)
- Scores each candidate from 0–100 based on job fit
- Ranks all applicants from best to worst
- Answers candidate questions about the job via a chatbot

---

## ✨ Features

| Feature | Description |
|---|---|
| 📄 Resume Reader | Extracts text from PDF and DOCX files |
| 🎯 Scoring Engine | AI scores resume vs job description (0–100) |
| 🏆 Ranker | Sorts candidates by score automatically |
| 💬 Chatbot | Answers candidate questions about the job |
| 🔄 ReAct Agent | Think → Act → Observe decision loop |
| 🚀 REST API | FastAPI server with full Swagger documentation |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10 |
| AI Model | Groq — LLaMA 3.1 8B Instant |
| API Framework | FastAPI + Uvicorn |
| Resume Parsing | pdfplumber + python-docx |
| Environment | python-dotenv |
| API Docs | Swagger UI (auto-generated) |

---

## 📁 Project Structure

```
smarthire-agent/
│
├── main.py              ← FastAPI server (entry point)
├── agent.py             ← ReAct loop (the brain)
├── resume_reader.py     ← Tool 1: extract text from PDF/DOCX
├── scorer.py            ← Tool 2: score resume 0-100
├── ranker.py            ← Tool 3: sort candidates by score
├── chatbot.py           ← Tool 4: answer job questions
├── memory.py            ← Conversation and session memory
├── requirements.txt     ← All dependencies
├── .env                 ← API keys (not pushed to GitHub)
└── .gitignore           ← Ignored files
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Groq API key (free at [https://console.groq.com](https://console.groq.com))

<!--### Installation

**1. Clone the repository**
```bash
git clone https://github.com/your-username/smarthire-agent.git
cd smarthire-agent
```

**2. Create and activate virtual environment**
```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Create your `.env` file**
```env
GROQ_API_KEY=your-groq-api-key-here
```

**5. Run the server**
```bash
uvicorn main:app --reload
```

**6. Open API docs in browser**
```
http://localhost:8000/docs
```

---

## 📡 API Endpoints

### `GET /`
Check if the agent is running.

**Response:**
```json
{
  "message": "SmartHire AI Agent is running!",
  "version": "1.0.0",
  "endpoints": [
    "POST /score-resume",
    "POST /rank-candidates",
    "POST /chat"
  ]
}
```

---

### `POST /score-resume`
Upload a resume and job description to get an AI score.

**Form Data:**
| Field | Type | Description |
|---|---|---|
| `file` | File | Resume in PDF or DOCX format |
| `job_description` | String | The job requirements text |

**Response:**
```json
{
  "task": "score",
  "result": {
    "score": 85,
    "strengths": ["Strong Python skills", "ML experience"],
    "weaknesses": ["No leadership experience"],
    "summary": "Strong AI engineer candidate with relevant experience"
  }
}
```

---

### `POST /rank-candidates`
Rank a list of candidates by their scores.

**Form Data:**
| Field | Type | Description |
|---|---|---|
| `candidates` | JSON String | List of candidates with scores |
| `top_n` | Integer | Number of top candidates to return |

**Request example:**
```json
[
  {"name": "Sara Ali",   "score": 91, "summary": "Senior ML engineer"},
  {"name": "Omar Hassan","score": 78, "summary": "Backend developer"},
  {"name": "Nour Ahmed", "score": 85, "summary": "AI engineer"}
]
```

**Response:**
```json
{
  "task": "rank",
  "result": [
    {"rank": 1, "name": "Sara Ali",   "score": 91},
    {"rank": 2, "name": "Nour Ahmed", "score": 85},
    {"rank": 3, "name": "Omar Hassan","score": 78}
  ]
}
```

---

### `POST /chat`
Ask the AI chatbot a question about a specific job.

**Form Data:**
| Field | Type | Description |
|---|---|---|
| `job_description` | String | The job posting text |
| `question` | String | The candidate's question |

**Response:**
```json
{
  "task": "chat",
  "result": {
    "answer": "The salary for this position is between 15,000 - 25,000 EGP per month."
  }
}
```
-->
---

## 🧠 How It Works — ReAct Agent Loop

The agent uses the **ReAct pattern** (Reason + Act) to process tasks:

```
Input received
     ↓
  [THINK] — Understand what needs to be done
     ↓
  [ACT]   — Call the right tool
     ↓
  [OBSERVE] — Read the result
     ↓
  Done? → YES → Return final answer
        → NO  → Loop back to THINK
```

**Example flow for scoring a resume:**
```
[THINK]   → I need to extract text from the resume first
[ACT]     → Calls resume_reader.extract_text()
[OBSERVE] → Got 2,400 characters of text
[THINK]   → Now I need to score it against the job description
[ACT]     → Calls scorer.score_resume()
[OBSERVE] → Score received: 85/100
[DONE]    → Return result to API
```

---

## 👥 Team

This project is part of the **SmartHire** system — an AI-powered HR recruitment platform.

| Role | Component |
|---|---|
| AI Agent (this repo) | Resume scoring, ranking, chatbot |
| Backend | Node.js + Express APIs |
| Frontend | React.js dashboard |
| Automation | n8n workflows |
| Database | PostgreSQL |
