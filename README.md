# AdGenius: Conversational AI for AdTech Support

**AdGenius** is a cloud-native conversational agent designed to automate Tier-1 support queries for high-volume advertising accounts. It integrates **Dialogflow CX** for Natural Language Understanding (NLU) with **Google Cloud Functions** for backend fulfillment, simulating a real-world enterprise support environment.

## 🚀 Project Goal
To reduce manual workload for Account Managers by automating routine tasks:
1.  **Performance Retrieval:** Fetching live metrics (CTR, Clicks, Cost) for specific campaigns.
2.  **Budget Management:** Authenticated budget updates via conversation.
3.  **Ticket Automation:** Instant creation of support tickets for complex issues.

## 🛠️ Technical Architecture
* **Frontend/NLU:** Dialogflow CX (Flow-based conversation design)
* **Backend Fulfillment:** Google Cloud Functions (Python 3.11)
* **Integration:** Webhook-based JSON data exchange
* **Deployment:** Serverless (Cloud Run underlying infrastructure)

## 🧩 Key Features Implemented

### 1. Context-Aware Intent Handling
The agent uses `sessionInfo` parameters to maintain context. For example, if a user asks "How is the *Diwali* campaign?" and then says "Increase **its** budget," the agent knows "its" refers to the *Diwali* campaign.

### 2. Dynamic Fulfillment (Webhook)
Unlike static chatbots, AdGenius logic lives in a Python backend.
- **Tag-based Routing:** Uses `fulfillmentInfo.tag` to route requests to specific logic blocks (`get_campaign_performance`, `change_budget`).
- **Case-Insensitive Matching:** Implemented robust string handling to map user input (e.g., "diwali search") to backend keys ("Diwali Search").

### 3. Scalable Entity Management
Uses a custom `@campaign_name` entity to validate user input before it ever reaches the backend, reducing API load and error rates.

## 💻 How to Run

### Prerequisites
* Google Cloud Platform Account
* Dialogflow CX Agent

### Deployment
1.  Deploy the backend to Google Cloud Functions:
    ```bash
    gcloud functions deploy adgenius-fulfillment \
    --runtime python311 \
    --trigger-http \
    --allow-unauthenticated
    ```
2.  Configure the Webhook in Dialogflow CX to point to the trigger URL.
3.  Enable the webhook on specific Routes (e.g., `get_campaign_performance`).

## 📈 Future Improvements
* **Live API Integration:** Replace the mock Python dictionary with calls to the Google Ads API.
* **Authentication:** Implement OAuth2 to verify user identity before allowing budget changes.
