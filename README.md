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
```

### Core Components
| Component | Function |
| :--- | :--- |
| **Dialogflow CX** | Handles State Machines, Flow transition, and Slot Filling. |
| **Cloud Functions (Gen 2)** | Python 3.11 backend for business logic, data normalization, and API chaining. |
| **Firestore (Native)** | NoSQL database for persistent campaign state and session history. |
| **Vertex AI (Search)** | RAG pipeline to parse unstructured technical PDFs (Policy/Compliance). |
| **GitHub Actions** | CI/CD pipeline for automated testing and deployment to GCP. |

---

## 🚀 Key Features

### 1. Stateful Campaign Management (CRUD)
Unlike standard stateless bots, AdGenius manages the lifecycle of a campaign.
* **Multi-Turn Slot Filling:** Collects Name, Budget, and Location in a specific sequence.
* **Validation:** Python middleware sanitizes inputs (e.g., converting "diwali sale" -> "Diwali Sale") before DB commits.
* **Atomic Writes:** Uses Firestore transactions to ensure budget updates do not conflict.

### 2. Hybrid NLU (Deterministic + Probabilistic)
The agent uses a "Router" pattern to decide the best response method:
* **Deterministic (Rules):** Money/Action-related queries (e.g., "Increase budget") are routed to hard-coded Python functions to ensure 100% accuracy.
* **Probabilistic (GenAI):** Policy/Advice queries (e.g., "Why is my ad blocked?") are routed to **Vertex AI Data Stores**, which synthesize answers from uploaded PDF manuals using LLMs.

### 3. Rich User Experience (UX)
* **Telephony Gateway:** Enabled Voice IVR support for phone-based support.
* **Custom Payloads:** Returns Rich Cards (JSON) with visual chips and buttons instead of plain text.

### 4. CI/CD & DevOps
* Implemented **GitHub Actions** workflow (`deploy.yml`) to automatically authenticate with GCP Service Accounts and deploy the Cloud Function upon push to `main`.

---

## 🛠️ Code Structure

```bash
├── .github/workflows
│   └── deploy.yml       # CI/CD Pipeline for auto-deploy
├── main.py              # Core logic (Webhook entry point)
├── requirements.txt     # Dependencies (Flask, Firestore, Functions Framework)
├── README.md            # Documentation
└── assets/              # Architecture diagrams and screenshots
```

---

## 💻 Installation & Setup

### Prerequisites
* Google Cloud Platform Account (Billing Enabled)
* Dialogflow CX Agent
* Python 3.11+

### Local Development
1.  **Clone the repo:**
    ```bash
    git clone [https://github.com/aywhoosh/adgenius-cx-agent.git](https://github.com/aywhoosh/adgenius-cx-agent.git)
    cd adgenius-cx-agent
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run locally with Functions Framework:**
    ```bash
    functions-framework --target=dialogflow_webhook
    ```

### Deployment
To deploy manually (without CI/CD):
```bash
gcloud functions deploy adgenius-fulfillment \
--runtime python311 \
--trigger-http \
--allow-unauthenticated
```

---

## 🔮 Future Improvements
* **Authentication:** Implement OAuth2 to link specific Google accounts to campaign data.
* **Analytics Dashboard:** Connect BigQuery to Dialogflow logs to visualize "Call Deflection Rate."
* **Multilingual Support:** Enable Spanish and Hindi locales for global support.

---

**Author:** Ayush Jain
[LinkedIn](https://linkedin.com/in/byayushjain) | [Portfolio](https://github.com/aywhoosh)