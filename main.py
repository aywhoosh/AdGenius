import functions_framework
from flask import jsonify
from google.cloud import firestore
# TESTING GITHUB ACTIONS
# Initialize the Database Connection
# This happens outside the function so it's fast (reused across calls)
db = firestore.Client()

@functions_framework.http
def dialogflow_webhook(request):
    req = request.get_json(silent=True)
    tag = req.get("fulfillmentInfo", {}).get("tag")
    parameters = req.get("sessionInfo", {}).get("parameters", {})
    
    response_text = "System Error: Logic not found."

    # LOGIC BLOCK 1: Campaign Performance (With Rich Content)
    if tag == "get_campaign_performance":
        raw_campaign = parameters.get("campaign_name", "").lower()
        doc_ref = db.collection("campaigns").document(raw_campaign)
        doc = doc_ref.get()

        if doc.exists:
            stats = doc.to_dict()
            campaign_title = raw_campaign.title()
            
            # Return a "Custom Payload" instead of just text
            json_response = {
                "fulfillment_response": {
                    "messages": [
                        {
                            "payload": {
                                "richContent": [
                                    [
                                        {
                                            "type": "info",
                                            "title": campaign_title,
                                            "subtitle": f"Spend: ₹{stats.get('cost')} | Clicks: {stats.get('clicks')}",
                                            "image": {
                                                "src": {
                                                    "rawUrl": "https://cdn-icons-png.flaticon.com/512/3094/3094845.png"
                                                }
                                            }
                                        },
                                        {
                                            "type": "chips",
                                            "options": [
                                                {"text": f"Increase budget for {campaign_title}"},
                                                {"text": "Create Support Ticket"}
                                            ]
                                        }
                                    ]
                                ]
                            }
                        }
                    ]
                }
            }
            return jsonify(json_response)
            
        else:
            response_text = f"I checked the database, but campaign '{raw_campaign}' was not found."
            # Fallback to text for errors
            return jsonify({"fulfillment_response": {"messages": [{"text": {"text": [response_text]}}]}})
    # --- LOGIC 2: WRITE TO DB ---
    elif tag == "change_campaign_budget":
        raw_campaign = parameters.get("campaign_name", "").lower()
        amount = parameters.get("number")
        
        if raw_campaign and amount:
            doc_ref = db.collection("campaigns").document(raw_campaign)
            doc = doc_ref.get()
            
            if doc.exists:
                # This is the 'Scale Up' moment: We actually update the cloud database
                doc_ref.update({"cost": amount}) 
                response_text = f"Success. I have written the new budget (₹{amount}) to the Firestore database for {raw_campaign}."
            else:
                 response_text = f"Cannot update budget. Campaign '{raw_campaign}' does not exist in the database."
        else:
            response_text = "Missing campaign name or amount."

    # --- LOGIC 3: TICKET (Unchanged) ---
    elif tag == "create_support_ticket":
        import random
        ticket_id = f"TKT-{random.randint(1000, 9999)}"
        response_text = f"Support ticket {ticket_id} created."
        
    # --- LOGIC 4: CREATE NEW CAMPAIGN (CRUD) ---
    elif tag == "create_campaign":
        # 1. Capture the two parameters we collected
        raw_name = parameters.get("new_campaign_name", "")
        raw_budget = parameters.get("new_campaign_budget")
        
        if raw_name and raw_budget:
            clean_name = raw_name.lower()
            
            # 2. Check if it already exists to avoid overwriting
            doc_ref = db.collection("campaigns").document(clean_name)
            doc = doc_ref.get()
            
            if doc.exists:
                response_text = f"Campaign '{clean_name}' already exists! Try a different name."
            else:
                # 3. Create the document in Firestore
                # We initialize clicks/conversions to 0 since it's new
                new_data = {
                    "cost": raw_budget,
                    "clicks": 0,
                    "conversions": 0,
                    "status": "Active"
                }
                doc_ref.set(new_data)
                response_text = f"Success! Campaign '{clean_name}' has been created with a budget of ₹{raw_budget}."
        else:
            response_text = "I couldn't capture the name or budget. Please try again."
    return jsonify({
        "fulfillment_response": {
            "messages": [{"text": {"text": [response_text]}}]
        }
    })