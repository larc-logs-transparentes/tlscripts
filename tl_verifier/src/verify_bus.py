import base64
import datetime
import json
import os

from utils.data_access_bu import get_bu_from_to_ids, get_global_tree_leaves_list, get_tree_data, get_all_local_tree_names
from pymerkle_logsTransparentes import MerkleTree


# Constants
RESULTS_DIR_NAME = "./tl_verifier/results"
RESULTS_FILE_NAME = "results_bu_verification.json"


# ### Methods to get local trees hashes in the global tree leaves ###
def get_local_tree_roots_from_global_tree(tree_name):
    leaves_list = get_global_tree_leaves_list()
    leaves_with_tree_name = []
    for leave in leaves_list:
        if leave.get('value').get('tree_name') == tree_name:
            leaves_with_tree_name.append(leave)
    return leaves_with_tree_name
# ###  --- end of -- Methods to get local trees hashes in the global tree leaves ###


# ###  Methods to get BUs ###
def get_leaf_index_range(tree_name):
    tree_data = get_tree_data(tree_name)
    tree_length = tree_data.get('length')
    tree_commitment_size = tree_data.get('commitment size')
    return {'start': 0, 'end': tree_length, 'commitment_size': tree_commitment_size}
# ###  --- end of -- Methods to get BUs ###


def get_array_of_whole_bu_strings(bus):
    bus_all_string = []
    for bu in bus:
        bus_all_string.append(bu['bu_inteiro'])
    return bus_all_string


def _build_tree_continuously(list_of_data, m_tree=None):
    if m_tree is None:
        m_tree = MerkleTree()

    for data in list_of_data:
        m_tree.append_entry(data)
    return m_tree


def get_bu_inteiro_list_between_ids(id_start, id_end, id_election):
    # get BUs from within the files
    bus = get_bu_from_to_ids(id_start, id_end, id_election)

    # get all bu_string only
    bu_string_list = [base64.b64decode(bu.get('bu').encode('ascii')) for bu in bus]
    # buse64_encoded = bu_string_list[0].encode('ascii')
    # buse64 = base64.b64decode(buse64_encoded)
    return bu_string_list
# ###  --- end of -- Methods to get BUs ###


# ###  Methods to get user input ###
def ask_user_which_election():
    local_tree_names = get_all_local_tree_names()
    for name in local_tree_names:
        print(name)

    user_input = input("Digite a eleição desejada: ")
    if user_input in local_tree_names:
        return user_input
    else:
        print(f'Não há eleições com o nome "{user_input}"')
        return False
# ###  --- end of -- Methods to get user input ###


# ### Methods to create results file
def create_results_file(results, tree_name):
    try:
        # Create dir to store BU files
        if not os.path.exists(RESULTS_DIR_NAME):
            os.makedirs(RESULTS_DIR_NAME)

        with open(f'{RESULTS_DIR_NAME}/{tree_name}_{RESULTS_FILE_NAME}', 'w') as file:
            json.dump(results, file, indent=4)  # indent=4 for pretty printing

    except Exception as e:
        raise Exception(f'Error creating results file: {e}')
# ### --- end of -- Methods to create results file


#  ## Core of the verify bus script
def verify_tree(tree_name):


    print('Reconstruindo a árvore...')

    # get starting id of BUs
    bus_index_range = get_leaf_index_range(tree_name)
    bus_id_start = bus_index_range.get('start')

    # get tree information from server
    local_tree_roots = get_local_tree_roots_from_global_tree(tree_name)       # get global tree leave (from local tree roots) with name
    local_tree_last_root = local_tree_roots[-1].get('value').get('value')    # last hash of tree in remote server

    # build local trees with BUs
    start_index = bus_id_start
    end_index = local_tree_roots[-1].get('value').get('tree_size') - 1
    bus = get_bu_inteiro_list_between_ids(start_index, end_index, tree_name)    # all BUs of interest
    local_tree = _build_tree_continuously(bus)              # build tree
    local_tree_root = local_tree.root.decode('utf-8')       # get root of tree just built

    print(f'Verificação realizada. Resultado: {local_tree_root == local_tree_last_root}')

    # make result of
    final_result = {
        "tree_name": tree_name, 
        "verification_result": local_tree_root == local_tree_last_root,
        "calculated_root": local_tree_root,
        "expected_root": local_tree_last_root
        }  
    create_results_file(final_result, tree_name)            # write it to file as JSON
    return final_result                                     # return dict


if __name__ == '__main__':
    start_time = datetime.datetime.now()
    # ask user which election (aka: tree name)
    tree_name = ask_user_which_election()
    if not tree_name:   # if election name is invalid, throws error
        raise Exception('Election name does not exist.')
    
    m_logs = verify_tree(tree_name)
    print(json.dumps(m_logs, indent=4))
    end_time = datetime.datetime.now()
    print(end_time - start_time)

