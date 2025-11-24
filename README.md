# AdGenius: Enterprise Conversational AI Agent (GCP)

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Python](https://img.shields.io/badge/python-3.11-blue)
![Platform](https://img.shields.io/badge/GCP-Serverless-orange)
![License](https://img.shields.io/badge/license-MIT-green)

> **A full-stack, stateful virtual agent designed to automate Tier-1 advertiser support, budget management (CRUD), and policy compliance using Hybrid NLU.**

---

## 📺 Demo Preview
[![Watch the Demo](https://img.youtube.com/vi/YOUR_VIDEO_ID_HERE/0.jpg)](https://www.youtube.com/watch?v=YOUR_VIDEO_ID_HERE)

---

## 💼 Business Problem
Large-scale advertising platforms face a significant bottleneck: Account Managers spend up to 40% of their time resolving repetitive Tier-1 queries ("What is my budget?", "Why was my ad rejected?").
**AdGenius** offloads these tasks to an AI agent that is:
1.  **Transactional:** Can read/write live budget data (not just answer FAQs).
2.  **Context-Aware:** Remembers campaign details across multi-turn conversations.
3.  **Omnichannel:** Accessible via Web Chat, Telephony, and API.

---

## 🏗️ Technical Architecture

The system utilizes a **Serverless Event-Driven Architecture** on Google Cloud Platform.

```mermaid
graph TD
    User((User)) -->|Voice/Text| CX[Dialogflow CX]
    CX -->|Intent Match| Webhook[Cloud Functions (Python)]
    CX -->|Fallback/Knowledge| Vertex[Vertex AI (RAG)]
    
    Webhook -->|Read/Write| DB[(Firestore NoSQL)]
    Webhook -->|Logs| Logging[Cloud Logging]
    
    Vertex -->|Index| Storage[Cloud Storage (PDFs)]
    
    subgraph "Data & Logic Layer"
    Webhook
    DB
    end
    
    subgraph "GenAI Layer"
    Vertex
    Storage
    end