import json

county_codes = json.load(open("/home/gfumagali/Documents/tlscripts/tl_sum/src/assets/county_codes_hash.json", "r"))


def get_state_from_code(code):
    """
    Retorna o estado de um BU.
    """
    try:
        return county_codes[str(code)]['uf']
    except KeyError:
        return 'ZZ'
