import datetime
import json
import os
import requests


# Constants
URL = 'http://localhost:8080/'
DIR_NAME_BUS = 'bus'


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


def get_last_downloaded_bu_id():
    # check if directory exists
    if os.path.exists(DIR_NAME_BUS) and os.path.isdir(DIR_NAME_BUS):
        files_names = os.listdir(DIR_NAME_BUS)  # list file names in dir
    else:   # if it does not, create it and return last id 0
        os.makedirs(DIR_NAME_BUS)
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
def create_files_from_bus(tree_length, step):
    try:
        # Create dir to store BU files
        if not os.path.exists(DIR_NAME_BUS):
            os.makedirs(DIR_NAME_BUS)

        # Set id_start to the next bu id, after the last bu id downloaded
        id_start = get_last_downloaded_bu_id() + 1

        # Set ids for first chunk
        step_local = step - 1
        id_start_local = id_start
        id_end_local = id_start_local + step_local

        # For each chunk (size "step")
        for i in range(id_start, tree_length, step):
            file_name = f'{DIR_NAME_BUS}/bus_{str(id_start_local).zfill(7)}_{str(id_end_local).zfill(7)}.json'  # create file
            data = get_bus_id_range(id_start_local, id_end_local)   # download BUs of chunk

            # Write BUs to file
            with open(file_name, 'a') as file:
                json.dump(data, file, indent=4)  # indent=4 for pretty printing

            # set IDs for next chunk
            id_start_local += step
            id_end_local = id_start_local + step_local

            # Print progress
            print(f'{id_start_local}/{tree_length}')
        print(f'{tree_length}/{tree_length}')     # Print finished
    except Exception as e:
        raise f'Error creating files: {e}'


def create_all_files_from_tree(tree_name):
    tree_data = get_tree_data(tree_name)
    tree_length = tree_data.get('length')
    tree_commintment_size = tree_data.get('commitment size')
    create_files_from_bus(tree_length, tree_commintment_size)


if __name__ == '__main__':
    start_time = datetime.datetime.now()
    create_all_files_from_tree('bu_tree')
    end_time = datetime.datetime.now()
    print(end_time - start_time)
