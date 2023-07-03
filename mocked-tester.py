import requests
from tlverifier.merkle_functions.data_access import get_proof, get_global_root, get_data     
from tlverifier.merkle_functions.tl_functions import verify_single_data
import tlverifier

proof = get_proof()     
trustable_global_root = get_global_root()
data = get_data()       
result = tlverifier.verify_single_data(proof, trustable_global_root, data)
print(result)
