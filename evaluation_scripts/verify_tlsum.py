from tl_sum.src.bu_functions import soma_votos
from tl_sum.src.service.json_utils import get_json_data_from_dir
import pathlib


import time
import pandas as pd

# Measure the time to sum bus
if __name__ == "__main__":

    BUS_PATH = '../results_2t'
    bus_per_sum = [1000, 10000, 50000, 100000, 200000, 300000, 400000, 472027]
    samples_per_sum = 5

    df = pd.DataFrame(index=bus_per_sum, columns=[f'sample_{i}' for i in range(0, samples_per_sum)])

    for limit_bus in bus_per_sum:
        samples = []
        for i in range(0, samples_per_sum):

            start = time.time()
            files, bus_json = get_json_data_from_dir(pathlib.Path(BUS_PATH))
            soma_votos(bus_json, verbose=False, _limit_bus=limit_bus)
            for f in files:
                f.close()
            end = time.time()
            samples.append(end - start)

        df.loc[limit_bus] = samples
        print(f'Time to sum {limit_bus} bus: {end - start} seconds')
    df.to_csv('sum_bus.csv')
