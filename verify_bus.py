import json
import os

from pymerkle_logsTransparentes import MerkleTree, MerkleProof, verify_inclusion, verify_consistency


# ### Methods to get local trees hashes in the global tree leaves ###
def get_local_tree_name():
    return 'bu_tree'


def get_global_tree_leaves_list():
    file_path = 'verify_bus_mock/v1/global_tree_leaves.json'

    file = open(file_path, "r")  # open file
    json_file = json.loads(file.read())
    file.close()
    return json_file['leaves']


def get_global_tree_leaves_with_tree_name(tree_name):
    leaves_list = get_global_tree_leaves_list()
    leaves_with_tree_name = []
    for leave in leaves_list:
        if leave['value']['tree_name'] == tree_name:
            leaves_with_tree_name.append(leave)
    return leaves_with_tree_name
# ###  --- end of -- Methods to get local trees hashes in the global tree leaves ###


# ###  Methods to get BUs ###
def get_leaf_index_range():
    return {'start': 0, 'end': 256}


def _get_filenames_of_bus_in_order(path):
    files_names = os.listdir(path)
    files_names.sort()
    return files_names


def _get_bus_in_file(path, bu_file_name):
    file_path = path + bu_file_name
    file = open(file_path, 'r')  # open file
    json_file = json.loads(file.read())
    file.close()
    bus = json_file
    return bus


def get_bu_from_to_ids(id_start, id_end):
    path = 'verify_bus_mock/v1/bus/'
    file_names = _get_filenames_of_bus_in_order(path)

    bus_in_range = []
    for file in file_names:
        bus = _get_bus_in_file(path, file)
        for bu in bus:
            if id_start <= bu.get('merkletree_leaf_index') < id_end:
                bus_in_range.append(bu)
    return bus_in_range
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


def build_local_tree():
    # get tree name
    tree_name = get_local_tree_name()

    # get id range of interest
    bus_index_range = get_leaf_index_range()
    bus_id_start = bus_index_range.get('start')
    bus_id_end = bus_index_range.get('end')

    # get all BUs as strings
    bus_all = get_bu_from_to_ids(bus_id_start, bus_id_end)
    bus_all_string = get_array_of_whole_bu_strings(bus_all)

    # get global tree leaves (local tree roots) with name
    global_tree_leaves = get_global_tree_leaves_with_tree_name(tree_name)

    # build local trees with BUs
    start_index = bus_id_start
    local_tree = None
    for global_leave in global_tree_leaves:                         # for each leave in global/root in local
        sub_tree_size = global_leave['value']['tree_size']          # get size S of tree
        bus = bus_all_string[start_index:sub_tree_size]             # get the next S elements of array in order
        local_tree = _build_tree_continuously(bus, local_tree)      # build the tree with S elements
        local_tree_root = local_tree.root.decode('utf-8')           # get root of local_tree
        print(len(bus), local_tree_root)
        start_index = sub_tree_size

    return 'blob'


if __name__ == '__main__':
    print(build_local_tree())
