import os
import requests
from dotenv import load_dotenv

load_dotenv()

class KrogerAPIClient:
    def __init__(self):
        self.client_id = os.getenv("KROGER_CLIENT_ID")
        self.client_secret = os.getenv("KROGER_CLIENT_SECRET")
        self.base_url = "https://api.kroger.com/v1"
        self.token_url = f"{self.base_url}/connect/oauth2/token"
        self.access_token = None

    def authenticate(self):
        """Fetch Client Credentials Access Token."""
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {"grant_type": "client_credentials", "scope": "product.compact"}

        response = requests.post(
            self.token_url, 
            headers=headers, 
            data=data, 
            auth=(self.client_id, self.client_secret)
        )
        response.raise_for_status()
        self.access_token = response.json()["access_token"]
        return self.access_token

    def search_products(self, term: str, limit: int = 10, location_id: str = "01400943"):
        """Fetch live products matching a term for a store location."""
        if not self.access_token:
            self.authenticate()

        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }
        params = {
            "filter.term": term,
            "filter.limit": limit,
            "filter.locationId": location_id
        }
        res = requests.get(f"{self.base_url}/products", headers=headers, params=params)
        res.raise_for_status()
        return res.json().get("data", [])