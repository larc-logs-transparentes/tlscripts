from tlverifier.merkle_functions.tl_functions import verify_data_entry
from evaluation_scripts.services.tl_manager_adapter import *
import time
import pandas as pd

# Measure the time to verify a data entry in a tree
if __name__ == "__main__":
    tree_name = 'tree_1000000'
    size = 1000000

    sizes_to_test = [100, 500, 1000]
    samples_per_size = 5

    df = pd.DataFrame(index=sizes_to_test, columns=[f'sample_{i}' for i in range(0, samples_per_size)])

    trustable_root = get_trustable_global_tree_root()['value']
    for size in sizes_to_test:
        samples = []
        for i in range(0, samples_per_size):
            start = time.time()
            for i in range(0, size):
                data_proof = get_data_proof(tree_name, i)
                result = verify_data_entry(data_proof, trustable_root, str(i))
                if not result['success']:
                    print(f'Verification failed at index {i}')
                    break
            end = time.time()
            samples.append(end - start)
        df.loc[size] = samples
        print(f'Time to verify {size} data entries: {end - start} seconds')
    df.to_csv('data_entry_verification.csv')
