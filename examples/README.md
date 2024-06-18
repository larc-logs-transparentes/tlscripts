# Examples

Module with examples of common verifications


## Utilitary Script: verify-consistency.py
Verify the consistency of all global and local trees

- Retrieves the global roots and the corresponding consistency proofs from server
- Check the consistency proofs
- Retrieves all leaves from global tree and find each local tree roots
- for each local tree, download the consistency proofs and check


```sh
# Run in terminal from /tlscripts :
python -m examples.src.verify-consistency
```

## Utilitary Script: verify-bu-inclusion.py
Verify the inclusion of a BU


- retrieves a bu from backend
- retrieves the corresponding proof
- verify the proof

```py
# Run in terminal from /tlscripts :
python -m examples.src.verify-bu-inclusion
```