import json
import requests
import os

from config import BACKEND_URL

# Constants
DIR_PATH_TREES = 'res/trees/'
ERROR_FILE_NAME = "results_bu_verification.json"
RESULTS_DIR_NAME = "../tl_verifier/results"


# ### Methods to connect to server
def generic_get_request(path):
    url = BACKEND_URL + path
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Request failed with status code {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
# ### --- end of -- Methods to connect to server


# ### Methods to get tree data ###
def get_all_local_tree_names():
    path = 'tree'
    response = generic_get_request(path)
    trees = response.get('trees')
    trees.remove('global_tree')
    trees.sort()
    return trees


def get_tree_data(tree_name):
    path = f'tree?tree_name={tree_name}'
    response = generic_get_request(path)
    return response


def get_global_tree_leaves_list():
    path = "tree/all-leaf-data-global-tree"
    response = generic_get_request(path)
    return response.get('leaves')
# ###  --- end of -- Methods to get tree data ###


# ###  Methods to get BUs ###
def get_leaf_index_range(index_start, index_end):
    return {'start': index_start, 'end': index_end}


def get_bu_from_to_ids(id_start, id_end, tree_name):   # Must download BUs (download_bus.py) before running this
    file_names = _get_files_containing_bu_ids(id_start, id_end, tree_name)

    if file_names is None:
        exception_text = f'Not all files with BUs within ids {id_start} and {id_end} were found'
        create_error_file(exception_text)
        raise Exception(exception_text)
    if id_end <= id_start:
        exception_text = f'Starting id must be higher than ending id (id_start = {id_start} and id_end = {id_end})'
        create_error_file(exception_text)
        raise Exception(exception_text)

    bus_in_range = []
    for file in file_names:
        bus = _get_bus_in_file(file, tree_name)
        # bus_of_interest = [bu for bu in bus if id_start <= bu.get('merkletree_leaf_index') <= id_end]
        bus_of_interest = [bu for bu in bus if id_start <= bu.get('merkletree_info').get('545').get('index') <= id_end]
        bus_in_range += bus
    return bus_in_range


def _get_filenames_of_bus_in_order(tree_name_dir):
    dir_path_TREES_complete = f'{DIR_PATH_TREES}{tree_name_dir}/'
    files_names = os.listdir(dir_path_TREES_complete)
    files_names.sort()
    return files_names


def _get_bus_in_file(bu_file_name, tree_name):
    file_path = DIR_PATH_TREES + tree_name + '/' + bu_file_name
    file = open(file_path, 'r')  # open file
    json_file = json.loads(file.read())
    file.close()
    bus = json_file
    return bus


# Gets BUs from downloaded BU files,
# It gets them from id_start to id_end of choice, even if range starts and ends in the middle of files
def _get_files_containing_bu_ids(id_start, id_end, id_election):
    files_of_interest = []

    # Gets all file names
    file_names = _get_filenames_of_bus_in_order(id_election)

    for file_name in file_names:
        # Gets range of BU ids in file
        file_id_range = get_ids_start_end_of_file_name(file_name)
        file_start_id = file_id_range.get('id_start')
        file_end_id = file_id_range.get('id_end')

        # if id_start is in file, appends file to files_of_interest
        if file_start_id <= id_start <= file_end_id:
            files_of_interest.append(file_name)

        # if id_start is not in file, but it was in previous file, then this file is also of interest
        if not file_start_id <= id_start <= file_end_id and len(files_of_interest) > 0:
            files_of_interest.append(file_name)

        # if id_end is in file, make sure file is in files_of_interest and returns
        if file_start_id <= id_end <= file_end_id:
            if file_name not in files_of_interest:
                files_of_interest.append(file_name)
            return files_of_interest

    return None


def get_ids_start_end_of_file_name(file_name):
    split_dot = file_name.split('.')[0].split('_')
    id_start = int(split_dot[0])
    id_end = int(split_dot[1])
    return {'id_start': id_start, 'id_end': id_end}

# ###  --- end of -- Methods to get BUs ###


# ### methods to create files of results when data_access fails
def create_error_file(error_msg):
    try:
        # Create dir to store BU files
        if not os.path.exists(RESULTS_DIR_NAME):
            os.makedirs(RESULTS_DIR_NAME)

        error_msg_dict = {'error': error_msg}

        with open(f'{RESULTS_DIR_NAME}/{ERROR_FILE_NAME}', 'w') as file:
            json.dump(error_msg_dict, file, indent=4)  # indent=4 for pretty printing

    except Exception as e:
        raise f'Error creating results file: {e}'
# ###  --- end of -- Methods to create error result file ###
