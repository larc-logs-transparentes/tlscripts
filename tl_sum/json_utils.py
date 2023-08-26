import ijson

def get_json_data(filename):
    f = open(filename, 'rb')
    objects = ijson.items(f, 'item')
    rows = (o for o in objects)
    return f, rows