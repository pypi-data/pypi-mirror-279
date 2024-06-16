import zlib
import json
import hashlib
import hmac

def compress_data(data):
    """
    Compresses data using zlib compression.

    Args:
        data (bytes): Data to compress.

    Returns:
        bytes: Compressed data.
    """
    return zlib.compress(data)

def decompress_data(data):
    """
    Decompresses data that was compressed using zlib compression.

    Args:
        data (bytes): Compressed data to decompress.

    Returns:
        bytes: Decompressed data.
    """
    return zlib.decompress(data)

def sign_transaction(transaction, wallet_key):
    """
    Signs a transaction dictionary using HMAC-SHA256.

    Args:
        transaction (dict): Transaction data to sign.
        wallet_key (str): Wallet key used for signing.

    Returns:
        dict: Transaction dictionary with added 'signature' field.
    """
    transaction_str = json.dumps(transaction, sort_keys=True)
    signature = hmac.new(wallet_key.encode(), transaction_str.encode(), hashlib.sha256).hexdigest()
    transaction['signature'] = signature
    return transaction

def verify_transaction(transaction):
    """
    Verifies the integrity of a signed transaction.

    Args:
        transaction (dict): Signed transaction dictionary.

    Returns:
        bool: True if the transaction's signature is valid, False otherwise.
    """
    signature = transaction.pop('signature', None)
    transaction_str = json.dumps(transaction, sort_keys=True)
    expected_signature = hmac.new(transaction['key'].encode(), transaction_str.encode(), hashlib.sha256).hexdigest()
    return signature == expected_signature
