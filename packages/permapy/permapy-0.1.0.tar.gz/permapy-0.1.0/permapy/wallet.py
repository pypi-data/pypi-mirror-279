import json
import os
import base64
import requests

class Wallet:
    def __init__(self, wallet_key=None):
        self.wallet_key = wallet_key

    def generate_wallet_key(self):
        """
        Generates a new wallet key securely.

        Returns:
            str: Newly generated wallet key.
        """
        self.wallet_key = base64.urlsafe_b64encode(os.urandom(32)).decode('utf-8')
        return self.wallet_key

    def save_wallet_key(self, path):
        """
        Saves the wallet key to a file.

        Args:
            path (str): Path to save the wallet key file.
        """
        with open(path, 'w') as f:
            json.dump({"wallet_key": self.wallet_key}, f)

    def load_wallet_key(self, path):
        """
        Loads the wallet key from a file.

        Args:
            path (str): Path to load the wallet key file from.

        Returns:
            str: Loaded wallet key.
        """
        with open(path, 'r') as f:
            data = json.load(f)
            self.wallet_key = data.get("wallet_key")
        return self.wallet_key

    def get_balance(self, address):
        """
        Retrieves the balance of a wallet address.

        Args:
            address (str): Wallet address to check balance.

        Returns:
            dict: JSON response containing wallet balance information.
        """
        try:
            url = f"https://arweave.net/wallet/{address}/balance"
            response = requests.get(url)
            response.raise_for_status()
            return response.json()

        except requests.RequestException as e:
            raise requests.RequestException(f"Error retrieving balance: {str(e)}")
