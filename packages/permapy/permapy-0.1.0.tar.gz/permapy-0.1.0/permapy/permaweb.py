import os
import requests
from .utils import compress_data, decompress_data

class Permaweb:
    def __init__(self, gateway_url="https://arweave.net"):
        self.gateway_url = gateway_url

    def upload_file(self, file_path, wallet_key, metadata=None):
        """
        Uploads a file to Permaweb via Arweave.

        Args:
            file_path (str): Path to the file to upload.
            wallet_key (str): Arweave wallet key for authentication.
            metadata (dict, optional): Metadata to include with the transaction.

        Returns:
            dict: JSON response containing transaction details.
        """
        try:
            with open(file_path, 'rb') as f:
                data = f.read()

            compressed_data = compress_data(data)

            payload = {
                "data": compressed_data,
                "key": wallet_key,
                "metadata": metadata
            }

            url = f"{self.gateway_url}/tx"
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()

        except IOError as e:
            raise IOError(f"Error reading file {file_path}: {str(e)}")

        except requests.RequestException as e:
            raise requests.RequestException(f"Upload failed: {str(e)}")

    def retrieve_file(self, tx_id, output_path):
        """
        Retrieves a file from Permaweb by transaction ID.

        Args:
            tx_id (str): Transaction ID of the file on Permaweb.
            output_path (str): Path to save the retrieved file.

        Returns:
            str: Path to the retrieved file.
        """
        try:
            url = f"{self.gateway_url}/{tx_id}"
            response = requests.get(url)
            response.raise_for_status()

            data = decompress_data(response.content)

            with open(output_path, 'wb') as f:
                f.write(data)

            return output_path

        except IOError as e:
            raise IOError(f"Error writing file to {output_path}: {str(e)}")

        except requests.RequestException as e:
            raise requests.RequestException(f"Retrieve failed: {str(e)}")
