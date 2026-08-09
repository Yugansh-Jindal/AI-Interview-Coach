# 🤖 AI Interview Coach

An AI-powered interview preparation platform that simulates technical interviews using Retrieval-Augmented Generation (RAG). The application analyzes a candidate's resume and job description to generate personalized interview questions, evaluates responses using LLMs, and provides detailed feedback with analytics and downloadable reports.

---

## ✨ Features

- 🔐 User Authentication
- 📄 Resume Upload
- 💼 Job Description Upload
- 🧠 RAG-powered Context Retrieval
- 🤖 AI-generated Interview Questions
- 📝 AI Answer Evaluation
- 📊 Analytics Dashboard
- 📈 Score History
- 📚 Topic Performance
- 📜 Interview History
- 📄 PDF Report Generation

---

## 🛠️ Tech Stack

### Frontend
- Streamlit

### Backend
- Python

### AI
- Groq LLM
- LangChain
- Sentence Transformers

### Vector Database
- ChromaDB

### Database
- SQLite

### PDF Processing
- PyMuPDF
- pdfplumber
- ReportLab

---

## 📂 Project Structure

```text
AI-Interview-Coach/
│
├── agents/
├── auth/
├── database/
├── pages/
├── rag/
├── services/
├── uploads/
├── app.py
├── requirements.txt
└── README.md