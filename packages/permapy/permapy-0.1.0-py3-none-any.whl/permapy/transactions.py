import requests
import json
from .utils import sign_transaction

class Transaction:
    def __init__(self, wallet_key, gateway_url="https://arweave.net"):
        self.wallet_key = wallet_key
        self.gateway_url = gateway_url

    def create_transaction(self, data, reward):
        """
        Creates a transaction dictionary for uploading data to Permaweb.

        Args:
            data (bytes): Data to upload.
            reward (str): Reward for mining the transaction.

        Returns:
            dict: Transaction dictionary.
        """
        payload = {
            "data": data,
            "reward": reward,
            "key": self.wallet_key
        }
        return payload

    def sign_and_submit_transaction(self, transaction_payload):
        """
        Signs and submits a transaction to Permaweb.

        Args:
            transaction_payload (dict): Transaction payload to sign and submit.

        Returns:
            dict: JSON response containing transaction details.
        """
        try:
            signed_transaction = sign_transaction(transaction_payload, self.wallet_key)

            url = f"{self.gateway_url}/tx"
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, headers=headers, json=signed_transaction)
            response.raise_for_status()
            return response.json()

        except requests.RequestException as e:
            raise requests.RequestException(f"Transaction submission failed: {str(e)}")
