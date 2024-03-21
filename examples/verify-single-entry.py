import requests
import tlverifier
import json
import utils
from config import TLMANAGER_URL as URL

DATA = "leaf" 
TREE = "tree1"

def main():
    leaf = setup()
    
    data_proof = utils.get_data_proof(leaf["index"], TREE)
    root = utils.get_global_root()

    result = tlverifier.verify_data_entry(data_proof, root["value"], DATA)

    if(result["success"] == True):
        print(f"Verify integrity of data '{DATA}' on {TREE}: ok")
    else:
        print(f"Verify integrity of data '{DATA}' on {TREE}: Failed")



def setup():
    create_tree(TREE)
    leaf = insert_leaf(DATA, TREE)
    commit_tree(TREE)
    return leaf

def create_tree(tree_name):
    payload = {
        "tree_name": tree_name,
        "commitment_size": 2
    }
    response = requests.post(URL + "tree-create", json=payload)
    json.loads(response.text)
    return

def insert_leaf(data, tree_name):
    payload = {
        "tree_name": tree_name,
        "data": data
    }
    response = requests.post(URL + "insert-leaf", json=payload)
    insert_leaf_response = json.loads(response.text)
    return insert_leaf_response

def commit_tree(tree_name):
    requests.post(URL + "tree/commit", json={"tree_name": tree_name})



if __name__ == "__main__":
    main()
