# BU Downloader

Module that downloads BUs, which will be verified


## Utilitary Script: download_bus.py
Downloads BUs from server for further usage in "verify_bus.py"

- Retrieves BU data from server
- Combine data in "commitment_size" chunks and save it as JSON files
-- It is able to stop downloading and restart from last one retrieved
- Save JSON files to res/bus directory
```sh
# Run in terminal from /tlscripts :
python -m bu_downloader.src.download_bus
```

## Utilitary Script: data_access_bu.py
Accesses BU data from JSON files created by "download_bus.py" (above)

- To get BUs data from a BU with id "id_start" to BU with id "id_end", call function:
```py
get_bu_from_to_ids(id_start, id_end)
```