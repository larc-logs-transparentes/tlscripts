import dataclasses
import ijson
import json

def get_json_data(filename):
    f = open(filename, 'rb')
    objects = ijson.items(f, 'item')
    rows = (o for o in objects)
    return f, rows
        
def print_dict(dict, filename=None):
    if filename is not None:
        with open(filename, 'w') as outfile:
            json.dump(dict, outfile, indent=4, cls=_EnhancedJSONEncoder, sort_keys=True)
    else:
        print(json.dumps(dict, indent=4, cls=_EnhancedJSONEncoder, sort_keys=True))
        
class _EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)