import json
import os


county_codes = json.load(open(os.path.join(os.path.dirname(__file__), 'county_codes_hash.json'), 'r'))


def get_state_from_code(code):
    """
    Retorna o estado de um BU.
    """
    try:
        return county_codes[str(code)]['uf']
    except KeyError:
        return 'ZZ'
