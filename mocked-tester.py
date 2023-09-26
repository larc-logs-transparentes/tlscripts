import tlverifier

proof = tlverifier.get_dummie_proof()                       # get proof from the tlmanager
global_root = tlverifier.get_dummie_trusted_global_root()   # get trustable root (e.g., from a monitor)
data = tlverifier.get_dummie_data()                         # get data to verify (e.g., BU)

result = tlverifier.verify_data_entry(proof, global_root, data)

print(result)
