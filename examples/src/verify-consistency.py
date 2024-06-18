import requests
import tlverifier
import json
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
    root_list = get_request(URL + "global-tree/all-roots")
    return root_list

def get_all_consistency_proof(tree_name):
    proofs = get_request(URL + "all-consistency-proof", params={
        "tree_name": tree_name
    })
    return proofs

def get_all_global_tree_leaf():
    all_leaf = get_request(URL + "global-tree/all-leaf-data")
    return all_leaf

def get_local_tree_list():
    tree_list = get_request(URL)["trees"]
    tree_list.remove('global_tree')
    tree_list = remove_empty_trees(tree_list)
    return tree_list

def remove_empty_trees(tree_list):
    for tree in tree_list:
        tree_info = get_request(URL + "tree", params={
            "tree_name": tree
        })
        if (tree_info["length"] == 0):
            tree_list.remove(tree)
    return tree_list

def get_request(url, params=None):
    print(f"GET {url} {params}")
    response = requests.get(url, params=params)
    return json.loads(response.text)

if __name__ == "__main__":
    main()

