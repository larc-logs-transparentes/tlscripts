from tl_downloader.src.download_bu import download_bu, ask_user_which_election
from tl_preprocessor.src.bu_preprocessor import preprocess_bus
from tl_verifier.src.verify_bus import verify_tree
import time
from tl_sum.src.service.json_utils import get_json_data_from_dir
from tl_sum.src.bu_functions import soma_votos
from pathlib import Path
import os
import pandas as pd

samples = 1
tree_name = "eleicao_545"

df = pd.DataFrame(index=[i for i in range(0, samples)], columns=['download_bus', 'rebuild tree', 'preprocess', 'sum'])

for i in range(0, samples):
    os.system('rm -rf res')
    execution_times = []

    print(f'Iteration {i}')

    print("Starting download")
    start_time = time.time()
    download_bu(tree_name)
    end_time = time.time()
    execution_times.append(end_time - start_time)
    print(f"Download finished in {end_time - start_time} seconds")

    print("Starting verification")
    start_time = time.time()
    result = verify_tree(tree_name)
    if(result['verification_result']==False):
        exit()
    end_time = time.time()
    execution_times.append(end_time - start_time)
    print(f"Verification finished in {end_time - start_time} seconds")

    print("Starting preprocessing")
    start_time = time.time()
    preprocess_bus('./res/trees/' + tree_name, './res/preprocessed_bu_jsons/' + tree_name)
    end_time = time.time()
    execution_times.append(end_time - start_time)
    print(f"Preprocessing finished in {end_time - start_time} seconds")

    print("Starting sum")
    start_time = time.time()
    files, bus_json = get_json_data_from_dir(Path('./res/preprocessed_bu_jsons/' + tree_name))
    resultado = soma_votos(bus_json)
    for f in files:
        f.close()
    end_time = time.time()
    execution_times.append(end_time - start_time)
    print(f"Sum finished in {end_time - start_time} seconds")

    df.loc[i] = execution_times

    print()

df.loc['mean'] = df.mean()
df.loc['std'] = df.std()

print(df)

df.to_csv(f'bu_full_verification_times_{tree_name}.csv')



