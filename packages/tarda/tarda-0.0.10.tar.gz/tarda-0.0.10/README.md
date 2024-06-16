# Tarda - An Intrusion Detection System Library

Tarda is a library for the collection of Intrusion 
Detection Systems (IDS) and robust-IDS, along with tools for evaluating them.

## Installation

You can install Tarda using pip:

```bash

pip install tarda
# Import the Tarda library
from tarda import AwesomeIDS

# Create an instance of the AwesomeIDS class
model = AwesomeIDS()

# Example: Parsing data from a pcap file
model.parse("path/to/your/file.pcap", "output/file.csv", save_netstat="output/netstat.pkl")

# Example: Training the model
train_params = {
    "path": "output/file.csv",
    "packet_limit": 20000,
    "maxAE": 10,
    "FMgrace": 16000,
    "ADgrace": 4000,
    "model_path": "output/kitsune.pkl",
    "normalize": True
}
model.train_model(train_params)

# Example: Testing the model
benign_pos, _ = model.test_model("output/file.csv", "output/kitsune.pkl", threshold=None, out_image="output/benign.png", record_scores=True)


