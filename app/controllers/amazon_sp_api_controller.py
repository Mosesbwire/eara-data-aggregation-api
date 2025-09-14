from flask import request,jsonify

from clients.amazon_sp_client import AmazonSPClient
from services.amazon_sp_api_service import AmazonSPService

amazon_sp_client = AmazonSPClient()
amazon_sp_service = AmazonSPService(amazon_sp_client)

def verify_order(order_id: str):
    """
    Endpoint to verify if an order exists in the Amazon Selling Partner system.

    Expects a JSON payload with the following structure:
    {
        "order_id": "string"  # The ID of the order to verify
    }

    Returns:
        JSON response indicating whether the order exists or not.
    """
    
    if not order_id:
        return jsonify({"error": "Missing 'order_id' in request body"}), 400

    try:
        exists = amazon_sp_service.verify_order(order_id)
        
        return jsonify({"order_id": order_id, "exists": exists}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

def get_access_token():
    """
    Endpoint to get a valid access token for the Amazon SP-API.

    Returns:
        JSON response containing the access token.
    """
    try:
        token = amazon_sp_service.get_access_token()
        return jsonify({"access_token": token}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500