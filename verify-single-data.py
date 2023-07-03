import requests
# Será que a gente consegue fazer esse import de maneira mais fácil?
from tlverifier.merkle_functions.tl_functions import verify_single_data
import json
import utils
from config import TLMANAGER_URL as URL


DATA = "leaf" 
TREE = "tree1"

def main():
    leaf = insert_leaf(DATA, TREE)
    commit_tree(TREE)

    data_proof = get_data_proof(leaf["index"], TREE)
    root = utils.get_trusted_root()

    result = verify_single_data(data_proof, root["value"], DATA)
    if(result["success"] == True):
        print(f"Verify integrity of data '{DATA}' on {TREE}: ok")
    else:
        print(f"Verify integrity of data '{DATA}' on {TREE}: Failed")


def insert_leaf(data, tree_name):
    payload = {
        "tree_name": tree_name,
        "data": data
    }
    response = requests.post(URL + "/insert-leaf", json=payload)
    insert_leaf_response = json.loads(response.text)
    return insert_leaf_response

def commit_tree(tree_name):
    requests.post(URL + "/tree/commit", json={"tree_name": tree_name})

def get_data_proof(index, tree_name):
    proof_response = requests.get(URL + "/data-proof", params={
        "tree_name": tree_name,
        "index": index
    })
    proof = json.loads(proof_response.text)
    return proof

if __name__ == "__main__":
    main()
