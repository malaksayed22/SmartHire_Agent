# 🤖 SmartHire — AI Recruitment Agent

![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.135-green)
![Groq](https://img.shields.io/badge/AI-Groq%20LLaMA-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

> AI-powered recruitment agent that automatically reads resumes, scores candidates, ranks applicants, and answers job-related questions — built with FastAPI and Groq AI.

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

| 🎯 Scoring Engine | AI scores resume vs job description (0–100) with strengths, weaknesses, experience level, and recommended action |
| 🏆 Ranker | Sorts candidates by score automatically and returns top N |
| 💬 Chatbot | Answers candidate questions professionally with strict job-only rules |
| 🔄 ReAct Agent v1.1 | Upgraded Think → Act → Observe loop with full reasoning, validation, and memory logs |
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

[AGENT]   → SmartHire AI Agent — Task: SCORE
[THINK]   → I need to extract the resume text before I can evaluate the candidate
[ACT]     → Calling resume_reader...
[OBSERVE] → Successfully extracted 3,706 characters. Resume is ready for evaluation.
[THINK]   → Resume text is ready. Now I need to evaluate it against the job description.
[ACT]     → Calling scorer...
[OBSERVE] → Score: 82/100. Experience: Junior. Recommended action: Consider.
[THINK]   → Score of 82/100 with 3 strengths and 2 weaknesses. Complete
[DONE]    → Task 'score' completed successfully
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
