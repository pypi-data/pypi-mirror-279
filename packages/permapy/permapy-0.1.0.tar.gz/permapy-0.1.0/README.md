# permapy

permapy is a Python package designed to interact with the Arweave network and Permaweb, facilitating decentralized storage and retrieval of data, with a focus on supporting AI/ML models and datasets.

## How It Works

permapy leverages the Arweave network, a decentralized storage platform known as Permaweb, to securely store and retrieve data. Key functionalities include:

- **Upload and Retrieve Files**: Easily upload files to Permaweb and retrieve them using transaction IDs.
- **Wallet Management**: Manage wallet keys securely for transactions with the Arweave network.
- **AI/ML Support**: Specifically designed to handle AI/ML models and datasets, allowing researchers and developers to store and share their trained models and data securely on Permaweb.
- **Asynchronous and Synchronous Operations**: Supports both synchronous and asynchronous network operations for flexibility and efficiency.

## Why permapy?

In today's data-driven world, maintaining the integrity and accessibility of AI/ML models and datasets is crucial. permapy addresses these needs by providing:

- **Decentralized Storage**: Utilizes Permaweb to store data across a decentralized network, ensuring data permanence and resistance to censorship.
- **Security and Privacy**: Implements robust encryption and secure transaction handling, protecting sensitive AI/ML models and datasets.
- **Community and Collaboration**: Facilitates easy sharing and access to AI/ML resources, fostering collaboration among researchers and developers worldwide.

## Installation

You can install permapy using pip:

```bash
pip install permapy
```

### Usage

```python
from permapy.permaweb import Permaweb
from permapy.wallet import Wallet
import tensorflow as tf
import pandas as pd

# Step 1: Generate a wallet key
wallet = Wallet()
wallet_key = wallet.generate_wallet_key()

# Step 2: Define functions to train model and upload to Permaweb
def train_model_and_upload(model_path, dataset_path, wallet_key):
    # Example: Train model (using TensorFlow for illustration)
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(10, activation='relu', input_shape=(4,)),
        tf.keras.layers.Dense(3, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    # Example: Load dataset (using pandas for illustration)
    df = pd.read_csv(dataset_path)
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]

    model.fit(X, y, epochs=10)

    # Example: Save trained model
    model.save(model_path)

    # Step 3: Upload model and dataset to Permaweb
    permaweb = Permaweb()
    
    # Upload trained model
    response_model = permaweb.upload_model(model_path, wallet_key, metadata={'task': 'classification'})
    print('Model upload response:', response_model)

    # Upload dataset
    response_dataset = permaweb.upload_dataset(dataset_path, wallet_key, metadata={'purpose': 'training'})
    print('Dataset upload response:', response_dataset)

# Step 4: Call the function to train model and upload to Permaweb
train_model_and_upload('trained_model.h5', 'dataset.csv', wallet_key)


```
## Asynchronous Operation

```python
import asyncio
from permapy.async_client import AsyncArweaveClient
from permapy.wallet import Wallet

async def async_upload_model(model_path, wallet_key):
    async with AsyncArweaveClient() as client:
        permaweb = Permaweb()
        response = await permaweb.upload_model(model_path, wallet_key, metadata={'task': 'classification'})
        print('Model upload response:', response)

# Example asynchronous usage
loop = asyncio.get_event_loop()
loop.run_until_complete(async_upload_model('path/to/your/model.h5', wallet_key))
```




