from iroha.client import IrohaClient
from iroha.crypto import KeyPair

client = IrohaClient("http://localhost:8080")  # replace with your node URL
keypair = KeyPair.generate()  # or load with KeyPair.from_json(...)

print("Client and KeyPair loaded.")
