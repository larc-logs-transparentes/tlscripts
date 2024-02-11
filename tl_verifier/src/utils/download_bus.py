import datetime
import json
import os
import requests

from tl_verifier.src.utils.data_access_bu import get_all_local_tree_names

# Constants
URL = 'http://localhost:8080/'
DIR_DL_PATH_BUS = '../../res/bus/'


# Get request to URL/path
def generic_get_request(path):
    try:
        response = requests.get(URL + path)
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


# Get BUs from id_start to tree_length inclusive
def get_bus_id_range(id_start, id_end):
    path = f'bu/find_by_index_range?initial_index={id_start}&final_index={id_end}'
    response = generic_get_request(path)
    return response


def get_bus_election_in_range(election_id, id_start, id_end):
    path = f'bu/find_by_merkletree_index_range?initial_index={id_start}&final_index={id_end}&election_id={election_id}'
    response = generic_get_request(path)
    return response


def get_last_downloaded_bu_id(tree_name):
    # check if directory exists
    dir_path = f'{DIR_DL_PATH_BUS}{tree_name}'
    if os.path.exists(dir_path) and os.path.isdir(dir_path):
        files_names = os.listdir(dir_path)  # list file names in dir
    else:   # if it does not, create it and return last id 0
        os.makedirs(dir_path)
        return -1

    # in an existing dir, check if there are files
    if len(files_names) > 0:    # if there is, look for higher bu id number
        high_id = -1
        for file_name in files_names:
            id_number = int(file_name.split('_')[-1].split('.')[0])     # get int out of higher id in file_name
            if id_number > high_id:
                high_id = id_number     # save the highest number
    else:   # if there is not, return last id 0
        return -1

    return high_id  # return highest number


# get bus from server by chunks of size "step" and organize it in files
def create_files_from_bus(tree_name, tree_length, step):
    tree_download_path = DIR_DL_PATH_BUS + tree_name
    try:
        # Create dir to store BU files
        if not os.path.exists(tree_download_path):
            os.makedirs(tree_download_path)

        # Set id_start to the next bu id, after the last bu id downloaded
        id_start = get_last_downloaded_bu_id(tree_name) + 1

        # Set ids for first chunk
        step_local = step - 1
        id_start_local = id_start
        id_end_local = id_start_local + step_local

        # Get election_id from tree_name
        election_id = tree_name.split('_')[-1]

        # For each chunk (size "step")
        for i in range(id_start, tree_length, step):
            data = get_bus_election_in_range(election_id, id_start_local, id_end_local)  # download BUs of chunk
            last_bu_in_file = data[-1].get('merkletree_leaf_index')     # get id of last element to name file
            file_name = f'{tree_download_path}/bus_{str(id_start_local).zfill(7)}_{str(last_bu_in_file).zfill(7)}.json'  # create file

            # Write BUs to file
            with open(file_name, 'a') as file:
                json.dump(data, file, indent=4)  # indent=4 for pretty printing

            # set IDs for next chunk
            id_start_local += step
            id_end_local = id_start_local + step_local

            # Print progress
            print(f'{id_start_local - step}/{tree_length}')
        print(f'{tree_length}/{tree_length}')     # Print finished
    except Exception as e:
        raise Exception(f'Error creating files: {e}')


def create_all_files_from_tree(tree_name):
    tree_data = get_tree_data(tree_name)
    tree_length = tree_data.get('length')
    tree_commitment_size = tree_data.get('commitment size')
    create_files_from_bus(tree_name, tree_length, tree_commitment_size)


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


if __name__ == '__main__':
    start_time = datetime.datetime.now()
    user_tree_name = ask_user_which_election()
    if not user_tree_name:  # if election name is invalid, throws error
        raise Exception('Election name does not exist.')
    create_all_files_from_tree(user_tree_name)
    end_time = datetime.datetime.now()
    print(end_time - start_time)
