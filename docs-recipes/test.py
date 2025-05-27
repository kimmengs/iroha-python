from iroha2 import IrohaClient, KeyPair
from iroha2.data_model.predicate import PredicateBox, ValuePredicate

keypair = KeyPair.generate()
client = IrohaClient(keypair, base_url="http://127.0.0.1:8080")

target_account = "ed0120CE7FA46C9DCE7EA4B125E2E36BDB63EA33073E7590AC92816AE1E861B7048B03@hivefund"

predicate = PredicateBox.Value(
    path="payload.instructions.Instructions[0].Transfer.Asset.destination",
    value=ValuePredicate.Equals(target_account)
)

txs = client.find_transactions(predicate=predicate)
for tx in txs:
    print(tx.hash, tx.payload.instructions)
