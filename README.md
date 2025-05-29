# multi-agent-AI-system
a multi-agent AI system that accepts input in PDF, JSON, or Email (text) format, classifies the format and intent, and routes it to the appropriate agent. The system must maintain shared context (e.g., sender, topic, last extracted fields) to enable chaining and traceability.

# 🧠 Multi-agent AI System for Document Classification and Processing

The project is a ** multi-agent AI system ** that classifies and process inputs in ** PDF, Jasan, or email (lesson) **. Each input is classified by format and intentions, then rooted for a particular agent (email, json, or PDF) for further procedure. A light memory module (using sqlite) stores shared references for traceability and chaining.

,

## 🔍 purpose

> Accept the input (PDF, JSON, Email), classify it, remove the route for the appropriate agent, remove the structured data, and log to the results on a shared memory store.

,

## ⚙ System Architecture

### 🧭 classifier agent
- ** input: ** raw file, email text, or json.
- ** output: ** format (pdf/json/email) + intent (eg, RFQ, Complaint, Challan).
- ** Routing: ** Direct Processing Directs the agent.
- ** LLM use: ** [gemma] (https://labrary/gemma) Olama (locally moves).

,

### 📬 email agent
- extracts:
  - ** Sender **
  - **Intention**
  - ** request **
- format material for the use of CRM-style.
- Log for memory with conversation ID.

,

### 🧾 PDF agent
- Text extract from PDF.
- It uses LLM to determine:
  - Intentions (eg, invoices, regulation)
  - Field (eg, invoice number, amount)
  - Anomals (if any)
- Log results for memory.

,

### 🧩 json agent
- Constituted JSON accepts.
- Improvement to target the scheme.
- Flag missing or discrepant area.
- Log results for memory.

,

### 💾 shared memory module
- Uses ** sqlite ** (`shared_memory.db`).
- Store:
  - Source
  - Format
  - Timestamp
  - Conversation ID
  - Results extracted
- The entire conversation enables the thread or document flow to track.

,

## 🛠 tech stack

- ** Language: ** Python
- ** llm: ** [gemma 2b] (https://labrary/gemma) (local through local)
- ** memory: ** sqlite
,
