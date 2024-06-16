import aiohttp

class AsyncArweaveClient:
    def __init__(self, gateway_url="https://arweave.net"):
        self.gateway_url = gateway_url

    async def get_network_info(self):
        """
        Retrieves network information asynchronously.

        Returns:
            dict: JSON response containing network information.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.gateway_url}/info") as response:
                response.raise_for_status()
                return await response.json()

    async def post_data(self, data, wallet_key, metadata=None):
        """
        Posts data to Permaweb asynchronously.

        Args:
            data (bytes): Data to upload.
            wallet_key (str): Arweave wallet key for authentication.
            metadata (dict, optional): Metadata to include with the transaction.

        Returns:
            dict: JSON response containing transaction details.
        """
        url = f"{self.gateway_url}/tx"
        headers = {"Content-Type": "application/json"}
        payload = {
            "data": data,
            "key": wallet_key,
            "metadata": metadata
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as response:
                response.raise_for_status()
                return await response.json()

    async def get_data(self, tx_id):
        """
        Retrieves data from Permaweb asynchronously.

        Args:
            tx_id (str): Transaction ID of the data to retrieve.

        Returns:
            dict: JSON response containing retrieved data.
        """
        url = f"{self.gateway_url}/{tx_id}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.json()
