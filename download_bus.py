# import datetime
import json
import os
import requests


# Constants
URL = 'http://localhost:8080/'
DIR_NAME_BUS = 'bus_raw'


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


# Get BUs from id_start to id_end inclusive
def get_bus_id_range(id_start, id_end):
    path = f'bu/find_by_index_range?initial_index={id_start}&final_index={id_end}'
    response = generic_get_request(path)
    return response


# get bus from server by chunks of size "step" and organize it in files
def create_files_from_bus(id_start, id_end, step):
    try:
        # Create dir to store BU files
        if not os.path.exists(DIR_NAME_BUS):
            os.makedirs(DIR_NAME_BUS)

        # Set ids for first chunk
        step_local = step - 1
        id_start_local = id_start
        id_end_local = id_start_local + step_local

        # For each chunk (size "step")
        for i in range(id_start, id_end, step):
            file_name = f'{DIR_NAME_BUS}/bus_{id_start_local}_{id_end_local}.json'  # create file
            data = get_bus_id_range(id_start_local, id_end_local)   # download BUs of chunk

            # Write BUs to file
            with open(file_name, 'a') as file:
                json.dump(data, file, indent=4)  # indent=4 for pretty printing

            # set IDs for next chunk
            id_start_local += step
            id_end_local = id_start_local + step_local

            # Print progress
            print(f'{id_start_local}/{id_end}')
        print(f'{id_end}/{id_end}')     # Print finished
    except Exception as e:
        raise f'Error creating files: {e}'


# if __name__ == '__main__':
#     start_time = datetime.datetime.now()
#     create_files_from_bus(0, 1000, 100)
#     end_time = datetime.datetime.now()
#     print(end_time - start_time)
