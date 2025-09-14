from clients.amazon_sp_client import AmazonSPClient

class AmazonSPService:
    def __init__(self, client: AmazonSPClient):
        self.client = client

    def verify_order(self, order_id: str) -> bool:
        """
        Verify if an order exists in the Amazon Selling Partner system.

        Args:
            order_id (str): The ID of the order to fetch.
        """
        try:
            return self.client.verify_order(order_id)
        except Exception as e:
            raise e
    
    def get_access_token(self) -> str:
        """
        Get a valid access token for the Amazon SP-API.

        Returns:
            str: The access token.
        """
        return self.client._get_access_token()