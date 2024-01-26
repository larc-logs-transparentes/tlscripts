from verify_bus import _build_tree_continuously
from evaluation_scripts.services.tl_manager_adapter import *

import time
import pandas as pd


def get_global_tree_leaves_with_tree_name(global_tree_leaves, tree_name):
    leaves_with_tree_name = []
    for leave in global_tree_leaves:
        if leave.get('value').get('tree_name') == tree_name:
            leaves_with_tree_name.append(leave)
    return leaves_with_tree_name


# Measure the rebuild time of a local tree
if __name__ == "__main__":
    trees = get_trees()
    samples_per_tree = 5

    df = pd.DataFrame(index=trees.values(), columns=[f'sample_{i}' for i in range(0, samples_per_tree)])

    global_tree_leaves = get_all_leaf_data_global_tree()['leaves']
    for tree_name, size in trees.items():
        leaves_in_global_tree = get_global_tree_leaves_with_tree_name(global_tree_leaves, tree_name)
        list_of_data = [str(i) for i in range(0, size)]

        samples = []
        for i in range(0, samples_per_tree):
            start = time.time()
            local_tree = None
            start_index = 0
            for global_tree_leaf in leaves_in_global_tree:
                tree_size = global_tree_leaf['value']['tree_size']
                end_index = tree_size
                data = list_of_data[start_index:end_index]

                local_tree = _build_tree_continuously(data, local_tree)
                local_tree_root = local_tree.root.decode('utf-8')

                if local_tree_root != global_tree_leaf['value']['value']:
                    print(f'Verification failed at tree {tree_name} in sample {i}')
                    break

                start_index = end_index
            end = time.time()
            samples.append(end - start)
        df.loc[size] = samples
        print(f'Time to build tree {tree_name}: {end - start} seconds')
    df.to_csv('rebuild_tree.csv')
