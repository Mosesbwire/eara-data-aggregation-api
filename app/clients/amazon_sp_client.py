from datetime import datetime, timedelta
from dotenv import load_dotenv
from typing import Optional, Dict, Any, Union
from urllib.parse import urlencode
import os
import requests
import time


load_dotenv()

EARA_REGIONAL_END_POINT = "https://sellingpartnerapi-na.amazon.com"
SANDBOX_END_POINT = "https://sandbox.sellingpartnerapi-na.amazon.com"

class AmazonSPClient:
    """
    Client for interacting with the Amazon Selling Partner API.
    """
    def __init__(self):

        self.client_id = os.getenv("AMAZON_SP_CLIENT_ID")
        self.client_secret = os.getenv("AMAZON_SP_CLIENT_SECTRET")
        self.refresh_token = os.getenv("AMAZON_SP_TOKEN_REFRESH")
        
        if not all([self.client_id, self.client_secret, self.refresh_token]):
            raise ValueError("Missing one or more required Amazon SP-API credentials.")
        
        self._access_token = None
        self._token_expiry = None
        self.session = requests.Session()
        self.base_url = EARA_REGIONAL_END_POINT  # Change to EARA_REGIONAL_END_POINT for production

    def _get_access_token(self) -> str:
        """
        Retrieve an access token using the refresh token.
        """
        if self._access_token and self._token_expiry and time.time() < self._token_expiry:
            return self._access_token

        token_url = "https://api.amazon.com/auth/o2/token"
        payload = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        encoded_payload = urlencode(payload)
        
        headers = {
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
        }

        
        try:
            response = self.session.post(token_url, data=encoded_payload, headers=headers, timeout=120)
            
            response.raise_for_status()
            token_data = response.json()


            self._access_token = token_data["access_token"]
            self._token_expiry = time.time() + token_data.get("expires_in", 3600) - 60
            return self._access_token

        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Failed to obtain access token: {e}")

        
    def _make_api_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        data: Optional[Union[Dict, str]] = None,
        json_body: Optional[Dict] = None,
        content_type: str = "application/json"
    ) -> Dict[str, Any]:
        """
        Make an authenticated API request to the specified endpoint.
        """

        url = f"{self.base_url}{endpoint}"
        

        access_token = self._get_access_token()
        
        headers = {
            "x-amz-access-token": access_token,
            "user-agent": "MyApp/1.0 (Language=Python)",
            "Content-Type": content_type,
        }

        try:
            response = self.session.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                data=data,        
                json=json_body,   
                timeout=30
            )

            
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            if hasattr(e, "response") and e.response is not None:
                raise Exception(
                    f"Amazon SP-API request failed: {e.response.status_code} - {e.response.text}"
                )
            raise Exception(f"Amazon SP-API request failed: {str(e)}")

     
    def get_order_details(self, order_id: str) -> Dict[str, Any]:
        """
        Fetch order details for a specific order ID.

        Args:
            order_id (str): The ID of the order to fetch.
        """
        
        endpoint = f"/orders/v0/orders/{order_id}"
        return self._make_api_request("GET", endpoint)

    
    def verify_order(self, order_id: str) -> bool:
        """
        Verify if an order exists in the Amazon Selling Partner system.

        Args:
            order_id (str): The ID of the order to verify.

        Returns:
            bool: True if the order exists, False otherwise.    
        """
        try:
            order_details = self.get_order_details(order_id)
            payload = order_details.get('payload', {})
            return order_id == payload.get('AmazonOrderId', '')
        except Exception as e:
            raise e