# ✦ Persona Intelligence

<div align="center">

![Persona Intelligence Banner](https://img.shields.io/badge/Persona-Intelligence-a855f7?style=for-the-badge&logo=sparkles&logoColor=white)

**AI-powered people & company intelligence engine — synthesized in seconds.**

[![Python](https://img.shields.io/badge/Python-3.10+-3b82f6?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-10b981?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-ff4b4b?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Groq](https://img.shields.io/badge/Groq-LLaMA_3.1-f59e0b?style=flat-square&logo=meta&logoColor=white)](https://groq.com)
[![License](https://img.shields.io/badge/License-MIT-64748b?style=flat-square)](LICENSE)

[Demo](#-demo) · [Features](#-features) · [Quick Start](#-quick-start) · [Architecture](#-architecture) · [API Reference](#-api-reference)

</div>

---

## 🔍 What is Persona?

**Persona Intelligence** is a full-stack AI research assistant that lets you search any founder, investor, company, or public figure and receive an instant, structured intelligence briefing — complete with an executive summary, strategic insights, confidence scoring, and verified source citations.

It combines **real-time web search** (Tavily + DuckDuckGo + Wikipedia) with **LLM synthesis** (Groq / LLaMA 3.1) to deliver results that would otherwise take hours of manual research — in under a second.

```
Search "Elon Musk"  →  Executive Summary + Key Insights + Verified Sources  →  0.8s
```

---

## ✨ Features

| Feature | Description |
|---|---|
| ⚡ **Instant Profiles** | AI-synthesized executive briefings on any person or company |
| 🧠 **Multi-Source Fusion** | Pulls from Tavily, DuckDuckGo, and Wikipedia simultaneously |
| 📊 **Confidence Scoring** | Every result comes with a 0–100 reliability score |
| 🛡️ **Verified Citations** | All claims are backed by real, clickable source URLs |
| 🎨 **Premium Dark UI** | Glassmorphism design with animated gradients, built in Streamlit |
| 🔌 **REST API** | Clean FastAPI backend — plug into any frontend or workflow |
| 🚀 **Blazing Fast** | Powered by Groq's LPU inference for sub-second LLM responses |

---

## 🖥️ Demo

> Search for a founder, investor, company, or public figure and get a structured intelligence card in seconds.

```
┌─────────────────────────────────────────────────────┐
│  ✦ Persona Intelligence                             │
│─────────────────────────────────────────────────────│
│  [ Search people, companies, or topics...  ] [✦ Go] │
│─────────────────────────────────────────────────────│
│  📋 Executive Intelligence Briefing   ● High  92%  │
│     Two-paragraph AI-synthesized profile overview  │
│                                                     │
│  ⚡ Strategic Profile Insights                      │
│     1. Key achievement or career milestone         │
│     2. Notable investment or company founded        │
│                                                     │
│  🛡️ Verified Citations & Sources  (4 references)   │
│     🔗 en.wikipedia.org/wiki/...  →               │
│     🔗 techcrunch.com/...         →               │
└─────────────────────────────────────────────────────┘
```

---

## 🏗️ Architecture

```
┌──────────────┐     HTTP POST      ┌───────────────────────────────────┐
│  Streamlit   │  ────────────────▶ │         FastAPI Backend           │
│  Frontend    │  /api/profile      │                                   │
│  (app.py)    │ ◀────────────────  │  ┌─────────┐  ┌───────────────┐  │
└──────────────┘   JSON Response    │  │  Tavily │  │  DuckDuckGo   │  │
                                    │  │ Search  │  │  Free Engine  │  │
                                    │  └────┬────┘  └──────┬────────┘  │
                                    │       │               │           │
                                    │  ┌────▼───────────────▼────────┐  │
                                    │  │     Wikipedia API           │  │
                                    │  └────────────────┬────────────┘  │
                                    │                   │               │
                                    │  ┌────────────────▼────────────┐  │
                                    │  │   Groq LLaMA 3.1 8B Instant │  │
                                    │  │   (JSON-structured output)  │  │
                                    │  └─────────────────────────────┘  │
                                    └───────────────────────────────────┘
```

**Stack:**
- **Frontend** — Streamlit with custom CSS (glassmorphism, animations)
- **Backend** — FastAPI with Pydantic schema validation
- **Search** — Tavily API (premium) + DuckDuckGo (free) + Wikipedia API
- **LLM** — Groq Cloud (LLaMA 3.1 8B Instant) with JSON mode

---

## ⚙️ Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/your-username/persona-intelligence.git
cd persona-intelligence
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

Create a `.env` file in the project root:

```env
TAVILY_API_KEY=tvly-xxxxxxxxxxxxxxxxxxxx
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxx
```

> Get your keys: [Tavily](https://tavily.com) · [Groq](https://console.groq.com)

### 4. Start the FastAPI backend

```bash
uvicorn main:app --reload --port 8000
```

### 5. Launch the Streamlit frontend

```bash
# In a new terminal
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) and start searching. 🚀

---

## 📦 Requirements

```txt
streamlit
fastapi
uvicorn
requests
python-dotenv
tavily-python
groq
duckduckgo-search
wikipedia-api
pydantic
```

---

## 📡 API Reference

### `POST /api/profile`

Generate an intelligence profile for any search query.

**Request Body**

```json
{
  "query": "Sam Altman"
}
```

**Response Schema**

```json
{
  "status": "success",
  "confidence_score": 91,
  "summary": "Sam Altman is the CEO of OpenAI...",
  "insights": [
    "Co-founded Loopt at 19, later acquired for $43.4M",
    "Served as President of Y Combinator from 2014–2019"
  ],
  "sources": [
    "https://en.wikipedia.org/wiki/Sam_Altman",
    "https://techcrunch.com/..."
  ]
}
```

**Status Values**

| Status | Meaning |
|---|---|
| `success` | Profile found and synthesized |
| `not_found` | No public records found for the query |
| `error` | Backend processing error |

---

## 🗂️ Project Structure

```
persona-intelligence/
├── app.py           # Streamlit frontend (UI + CSS)
├── main.py          # FastAPI backend (search + LLM logic)
├── .env             # API keys (not committed)
├── requirements.txt # Python dependencies
└── README.md
```

---

## 🔑 Environment Variables

| Variable | Required | Description |
|---|---|---|
| `TAVILY_API_KEY` | ✅ Yes | Tavily web search API key |
| `GROQ_API_KEY` | ✅ Yes | Groq Cloud API key for LLaMA inference |

---

## 🛣️ Roadmap

- [ ] Entity type filters (Founders / Investors / Companies)
- [ ] Save & export profiles as PDF
- [ ] Persistent search history
- [ ] Batch search (multiple entities at once)
- [ ] LinkedIn and Crunchbase integrations
- [ ] Hosted cloud deployment (Streamlit Cloud + Railway)

---

## 🤝 Contributing

Contributions are welcome! Please open an issue first to discuss what you'd like to change.

```bash
# Fork → Clone → Branch → PR
git checkout -b feature/your-feature-name
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">

Built with ✦ by **Persona Intelligence** · Powered by Groq + Tavily + Streamlit

*Search smarter. Understand faster.*

</div>
