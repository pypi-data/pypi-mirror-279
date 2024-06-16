import requests

class ArweaveClient:
    def __init__(self, gateway_url="https://arweave.net"):
        self.gateway_url = gateway_url

    def get_network_info(self):
        """
        Retrieves network information from Arweave's gateway.

        Returns:
            dict: JSON response containing network information.
        """
        try:
            response = requests.get(f"{self.gateway_url}/info")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise requests.RequestException(f"Error fetching network info: {str(e)}")

    def post_data(self, data, wallet_key, metadata=None):
        """
        Posts data to Permaweb asynchronously.

        Args:
            data (bytes): Data to upload.
            wallet_key (str): Arweave wallet key for authentication.
            metadata (dict, optional): Metadata to include with the transaction.

        Returns:
            dict: JSON response containing transaction details.
        """
        try:
            url = f"{self.gateway_url}/tx"
            headers = {"Content-Type": "application/json"}
            payload = {
                "data": data,
                "key": wallet_key,
                "metadata": metadata
            }
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise requests.RequestException(f"Error posting data: {str(e)}")

    def get_data(self, tx_id):
        """
        Retrieves data from Permaweb asynchronously.

        Args:
            tx_id (str): Transaction ID of the data to retrieve.

        Returns:
            dict: JSON response containing retrieved data.
        """
        try:
            url = f"{self.gateway_url}/{tx_id}"
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise requests.RequestException(f"Error fetching data: {str(e)}")
