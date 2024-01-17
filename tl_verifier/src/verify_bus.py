import datetime
import json
import os

from utils.data_access_bu import get_bu_from_to_ids, get_global_tree_leaves_list, get_local_tree_name, get_tree_data
from pymerkle_logsTransparentes import MerkleTree


# Constants
RESULTS_DIR_NAME = "../results"
RESULTS_FILE_NAME = "results_bu_verification.json"


# ### Methods to get local trees hashes in the global tree leaves ###
def get_global_tree_leaves_with_tree_name(tree_name):
    leaves_list = get_global_tree_leaves_list()
    leaves_with_tree_name = []
    for leave in leaves_list:
        if leave.get('value').get('tree_name') == tree_name:
            leaves_with_tree_name.append(leave)
    return leaves_with_tree_name
# ###  --- end of -- Methods to get local trees hashes in the global tree leaves ###


# ###  Methods to get BUs ###
def get_leaf_index_range():
    tree_name = get_local_tree_name()
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


def get_bu_inteiro_list_between_ids(id_start, id_end):
    # get BUs from within the files
    bus = get_bu_from_to_ids(id_start, id_end)

    # get all bu_string only
    bu_string_list = [bu.get('bu_inteiro') for bu in bus]
    return bu_string_list
# ###  --- end of -- Methods to get BUs ###


# ### Methods to create results file
def create_results_file(results):
    try:
        # Create dir to store BU files
        if not os.path.exists(RESULTS_DIR_NAME):
            os.makedirs(RESULTS_DIR_NAME)

        with open(f'{RESULTS_DIR_NAME}/{RESULTS_FILE_NAME}', 'w') as file:
            json.dump(results, file, indent=4)  # indent=4 for pretty printing

    except Exception as e:
        raise f'Error creating results file: {e}'
# ### --- end of -- Methods to create results file


#  ## Core of the verify bus script
def build_whole_tree():
    # get tree name
    tree_name = get_local_tree_name()

    # get starting id of BUs
    bus_index_range = get_leaf_index_range()
    bus_id_start = bus_index_range.get('start')

    # get global tree leaves (local tree roots) with name
    global_tree_leaves = get_global_tree_leaves_with_tree_name(tree_name)

    # build local trees with BUs
    start_index = bus_id_start
    local_tree = None
    results_log = []
    results = True
    count = 0
    for global_leaf in global_tree_leaves:                      # for each leaf in global/root in local
        tree_size = global_leaf['value']['tree_size']           # get subtree size
        end_index = tree_size - 1                               # get last index of subtree
        bus = get_bu_inteiro_list_between_ids(start_index, end_index)   # get all strings of bus between start and end indexes
        local_tree = _build_tree_continuously(bus, local_tree)  # build the tree with bus with indexes in [start_index:end_index]
        local_tree_root = local_tree.root.decode('utf-8')       # calculate root of local_tree

        # organize partial results
        partial_result = {
            "tree_length": end_index,
            "calculated_tree_root": local_tree_root,
            "global_tree_leaf": global_leaf['value']['value']
        }

        # compare partial local root and partial global leaf
        if local_tree_root == global_leaf['value']['value']:
            partial_result["validation"] = True
            results_log.append(partial_result)  # log partial result
        else:
            partial_result["validation"] = False
            results_log.append(partial_result)  # log partial result
            results = False
            break

        start_index = tree_size    # update start_index
        count += 1
        print(count)    # print count, so we know it is still running

    final_result = {"result": results, "log": results_log}  # build final result dict
    create_results_file(final_result)                       # write it to file as JSON
    return final_result                                     # return dict


if __name__ == '__main__':
    start_time = datetime.datetime.now()
    m_logs = build_whole_tree()
    print(m_logs)
    end_time = datetime.datetime.now()
    print(end_time - start_time)

