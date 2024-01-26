from tlverifier.merkle_functions.tl_functions import verify_local_tree_history_consistency
from evaluation_scripts.tl_manager_adapter import *
import time
import pandas as pd

# Measure the time to verify consistency of a local tree
if __name__ == "__main__":
    trees = get_trees()
    samples_per_tree = 5

    df = pd.DataFrame(index=trees.values(), columns=[f'sample_{i}' for i in range(0, samples_per_tree)])

    all_leaf_global = get_all_leaf_data_global_tree()
    global_tree_root = get_trustable_global_tree_root()['value']
    for tree_name, size in trees.items():
        samples = []
        all_consistency_proof = get_all_consistency_proof(tree_name)
        for i in range(0, samples_per_tree):
            start = time.time()
            result = verify_local_tree_history_consistency(all_leaf_global, all_consistency_proof, global_tree_root, tree_name)
            end = time.time()
            samples.append(end - start)
            if not result['success']:
                print(f'Verification failed at tree {tree_name} in sample {i}')
                break
        df.loc[size] = samples
        print(f'Time to verify consistency of tree {tree_name}: {end - start} seconds')
    df.to_csv('local_tree_consistency_verification.csv')
