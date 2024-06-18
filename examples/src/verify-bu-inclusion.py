import requests
import tlverifier
import json
import base64
from config import BACKEND_URL as URL

BU_ID = "6661d95ca40c1f84d28bd6e2" 

def main():
    # setup
    bu = get_bu()
    root = get_global_root()
    
    # get inclusion proof for bu
    eleicao = bu["eleicoes"][0]
    index = bu["merkletree_info"][f"{eleicao}"]["index"]
    tree_name = bu["merkletree_info"][f"{eleicao}"]["tree_name"]
    data_proof = get_data_proof(index, tree_name)

    # decode bu from base64
    bu_base64 = bu["bu"]
    bu_binary = base64.b64decode(bu_base64.encode('ascii'))

    # verify integrity of bu
    result = tlverifier.verify_data_entry(data_proof, root, bu_binary)

    if(result["success"] == True):
        print(f"Verify integrity of bu: ok")
    else:
        print(f"Verify integrity of bu: Failed")
        print(result)


def get_bu():
    bu_response = requests.get(URL + "bu/find_by_id", params={"id": BU_ID})
    bu = json.loads(bu_response.text)
    return bu

def get_global_root():
    root_response = requests.get(URL + "tree/tree-root", params={"tree_name": "global_tree"})
    root = json.loads(root_response.text)["value"]
    return root

def get_data_proof(index, tree_name):
    proof_response = requests.get(URL + "tree/data-proof", params={
        "tree_name": tree_name,
        "index": index
    })
    proof = json.loads(proof_response.text)
    return proof

if __name__ == "__main__":
    main()
