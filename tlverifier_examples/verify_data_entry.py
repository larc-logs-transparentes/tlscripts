import json

import requests
import json
from tlverifier.merkle_functions.tl_functions import verify_data_entry
from pymerkle_logsTransparentes import MerkleTree

if __name__ == "__main__":
    bu_id = '657dad8f6468c416406772bb'

    URL_data = f'http://localhost:8080/bu/find_by_id?id={bu_id}'
    bu_data = requests.get(URL_data).json()
    bu_inteiro = bytes(json.dumps(bu_data['bu_inteiro']), 'utf-8')
    print(f'BU: {bu_inteiro}')
    print(f'Hash do BU: {MerkleTree().hash_entry(bu_inteiro)}')

    leaf_index = bu_data['merkletree_leaf_index']
    election = bu_data['id_eleicao']
    URL_data_proof = f'http://localhost:8080/tree/data-proof?tree_name=bu_tree_election_{election}&index={leaf_index}'
    data_proof = requests.get(URL_data_proof).json()

    URL_trustable_root = 'http://localhost:8080/tree/tree-root?tree_name=global_tree'
    global_root = requests.get(URL_trustable_root).json()['value']

    result = verify_data_entry(data_proof, global_root, bu_inteiro)
    print(result)