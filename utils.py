import requests
import json
from config import TLMANAGER_URL as URL


# get global root, from a trusted source (e.g., monitor)
def get_trusted_root():
    root_response = requests.get(URL + "/global-tree/root")
    root = json.loads(root_response.text)["root"]
    return root