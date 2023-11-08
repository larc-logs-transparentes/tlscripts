import json
import requests
import os


# Constants
DIR_PATH_BUS = 'bus_raw/'


def generic_get_request(path):
    url = "http://localhost:8080/" + path
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Request failed with status code {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


def get_tree_data(tree_name):
    path = f'tree?tree_name={tree_name}'
    response = generic_get_request(path)
    return response


# ### Methods to get local trees hashes in the global tree leaves ###
def get_local_tree_name():
    return 'bu_tree'


def get_global_tree_leaves_list():
    path = "global_tree/all-leaf-data"
    response = generic_get_request(path)
    return response.get('leaves')
# ###  --- end of -- Methods to get local trees hashes in the global tree leaves ###


# ###  Methods to get BUs ###
def get_leaf_index_range(index_start, index_end):
    return {'start': index_start, 'end': index_end}


def get_bu_from_to_ids(id_start, id_end):   # Must download BUs (download_bus.py) before running this
    file_names = _get_files_containing_bu_ids(id_start, id_end)

    if file_names is None:
        raise Exception(f'No files with BUs within ids {id_start} and {id_end} were found')
    if id_end <= id_start:
        raise Exception(f'Starting id must be higher than ending id (id_start = {id_start} and id_end = {id_end})')

    bus_in_range = []
    for file in file_names:
        bus = _get_bus_in_file(file)
        bus_of_interest = [bu for bu in bus if id_start <= bu.get('merkletree_leaf_index') < id_end]
        bus_in_range += bus_of_interest
    return bus_in_range


def _get_filenames_of_bus_in_order():
    path = 'bus_raw/'
    files_names = os.listdir(path)
    files_names.sort()
    return files_names


def _get_bus_in_file(bu_file_name):
    file_path = DIR_PATH_BUS + bu_file_name
    file = open(file_path, 'r')  # open file
    json_file = json.loads(file.read())
    file.close()
    bus = json_file
    return bus


def _get_files_containing_bu_ids(id_start, id_end):
    files_of_interest = []
    file_names = _get_filenames_of_bus_in_order()
    for file in file_names:
        bus = _get_bus_in_file(file)
        bu_start = [bu for bu in bus if bu.get('merkletree_leaf_index') == id_start]
        bu_end = [bu for bu in bus if bu.get('merkletree_leaf_index') == id_end]
        if bu_start:
            files_of_interest.append(file)
        if bu_start == [] and bu_end == [] and len(files_of_interest) > 0:
            files_of_interest.append(file)
        if bu_end:
            if file not in files_of_interest:
                files_of_interest.append(file)
            return files_of_interest
    return None

# ###  --- end of -- Methods to get BUs ###
