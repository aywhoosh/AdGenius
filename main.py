import functions_framework
from flask import jsonify

# Mock Database - keys are now lowercase for easier matching
CAMPAIGN_DATA = {
    "diwali search": {"clicks": 1200, "cost": 5000, "conversions": 85},
    "diwali remarketing": {"clicks": 450, "cost": 2100, "conversions": 30}
}

@functions_framework.http
def dialogflow_webhook(request):
    req = request.get_json(silent=True)
    
    # 1. Identify which "Tag" Dialogflow sent us
    tag = req.get("fulfillmentInfo", {}).get("tag")
    
    # 2. Extract parameters from the session
    parameters = req.get("sessionInfo", {}).get("parameters", {})
    
    response_text = "I'm not sure how to help with that specific request."

    # LOGIC BLOCK 1: Campaign Performance
    if tag == "get_campaign_performance":
        raw_campaign = parameters.get("campaign_name", "")
        # Convert user input to lowercase so it matches our database keys
        campaign_key = raw_campaign.lower()
        
        if campaign_key in CAMPAIGN_DATA:
            stats = CAMPAIGN_DATA[campaign_key]
            # We use .title() just to make the output look nice
            response_text = (f"Here is the performance for {campaign_key.title()}: "
                             f"{stats['clicks']} clicks, {stats['conversions']} conversions, "
                             f"at a cost of ₹{stats['cost']}.")
        else:
            response_text = f"I couldn't find data for the campaign: {raw_campaign}. Please check the name."

    # LOGIC BLOCK 2: Change Budget
    elif tag == "change_campaign_budget":
        raw_campaign = parameters.get("campaign_name", "")
        amount = parameters.get("number")
        
        if raw_campaign and amount:
            response_text = f"Done. I've updated the daily budget of {raw_campaign} to ₹{amount}."
        else:
            response_text = "I missed the campaign name or the amount. Could you repeat that?"

    # LOGIC BLOCK 3: Create Ticket
    elif tag == "create_support_ticket":
        import random
        ticket_id = f"TKT-{random.randint(1000, 9999)}"
        response_text = f"Support ticket created. Ticket ID: {ticket_id}. A specialist will email you shortly."

    # 3. Return the response in Dialogflow CX format
    json_response = {
        "fulfillment_response": {
            "messages": [
                {"text": {"text": [response_text]}}
            ]
        }
    }
    return jsonify(json_response)
