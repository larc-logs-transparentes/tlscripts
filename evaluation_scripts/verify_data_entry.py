from tlverifier.merkle_functions.tl_functions import verify_data_entry
from services.tl_manager_adapter import *
import time
import pandas as pd

# Measure the time to verify a data entry in a tree
if __name__ == "__main__":
    trees = get_trees()
    samples_per_tree = 50

    df = pd.DataFrame(index=trees.values(), columns=[f'sample_{i}' for i in range(0, samples_per_tree)])

    trustable_root = get_trustable_global_tree_root()['value']
    for (tree_name, size) in trees.items():
        samples = []
        for i in range(0, samples_per_tree):
            data_proof = get_data_proof(tree_name, 500)
            start = time.time()
            result = verify_data_entry(data_proof, trustable_root, str(500))
            end = time.time()
            if not result['success']:
                print(f'Verification failed at tree {tree_name} in sample {500}')
                break
            samples.append(end - start)
        df.loc[size] = samples
        print(f'Mean time to verify data entry in tree {tree_name}: {df.loc[size].mean()} seconds')
    df.to_csv('data_entry_verification.csv')
