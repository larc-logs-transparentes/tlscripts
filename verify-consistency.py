import requests
import tlverifier
import json
import utils
from config import TLMANAGER_URL as URL

def main():
    # get all global roots. Those represents the roots that the monitor has stored locally
    trusted_global_roots = get_all_global_roots() 
    
    global_tree_proofs = get_all_consistency_proof("global_tree")
    result = tlverifier.verify_global_tree_history_consistency(global_tree_proofs, trusted_global_roots)
    if(result["success"] == True):
        print("Verify consistency on global tree: ok")
    else:
        print("Verify consistency on global tree: Failed")
   

    latest_root = trusted_global_roots["roots"][-1]
    global_tree_data = get_all_global_tree_leaf()
    tree_list = get_local_tree_list()

    for tree in tree_list:
        local_tree_proofs = get_all_consistency_proof(tree)
        result = tlverifier.verify_local_tree_history_consistency(global_tree_data, local_tree_proofs, latest_root["value"], tree)
        if(result["success"] == True):
            print(f"Verify consistency on {tree}: ok")
        else:
            print(f"Verify consistency on {tree}: Failed")


def get_all_global_roots():
    response = requests.get(URL + "/global-tree/all-roots")
    root_list = json.loads(response.text)
    return root_list

def get_all_consistency_proof(tree_name):
    proofs_response = requests.get(URL + "/all-consistency-proof", params={
        "tree_name": tree_name
    })
    proofs = json.loads(proofs_response.text)
    return proofs

def get_all_global_tree_leaf():
    all_leaf_response = requests.get(URL + "/global-tree/all-leaf-data")
    all_leaf = json.loads(all_leaf_response.text)
    return all_leaf

def get_local_tree_list():
    tree_list_response = requests.get(URL)
    tree_list = json.loads(tree_list_response.text)["trees"]
    tree_list.remove('global_tree')
    tree_list = remove_empty_trees(tree_list)
    return tree_list

def remove_empty_trees(tree_list):
    for tree in tree_list:
        tree_response = requests.get(URL + "/tree", params={
            "tree_name": tree
        })
        tree_info = json.loads(tree_response.text)

        if (tree_info["length"] == 0):
            tree_list.remove(tree)
    return tree_list

if __name__ == "__main__":
    main()

