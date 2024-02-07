import requests
import json
from config import TLMANAGER_URL as URL


def get_global_root():
    root_response = requests.get(URL + "/global-tree/root")
    root = json.loads(root_response.text)["root"]
    return root

def get_data_proof(index, tree_name):
    proof_response = requests.get(URL + "/data-proof", params={
        "tree_name": tree_name,
        "index": index
    })
    proof = json.loads(proof_response.text)
    return proof