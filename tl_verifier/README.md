# TL Verifier

Module that verifies BUs


## Main Script: verify_bus.py
This script rebuilds trees to verify if given tree is valid in the following steps:

- Read downloaded BUs (explained later in "download_bus.py")
- Builds local trees
- Compare with remote trees
- Creates a file with result (success or fail with point of failure)
```sh
# Run in terminal from /tlscripts :
python -m tl_verifier.src.verify_bus
```
