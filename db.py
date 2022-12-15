import json
import os

def init(file):
    if not os.path.isfile(f'{file}.json'):
        f = open(f'{file}.json', 'w')
        json.dump({}, f)
        f.close()

def get_all(file):
    init(file)
    f = open(f'{file}.json', 'r')
    data = json.load(f)
    f.close()
    return data

def get_latest(file, num=1):
    init(file)
    data = get_all(file)
    keys = list(data.keys())
    keys.sort()
    keys = keys[-num:]
    result = {}
    for key in keys:
        result[key] = data[key]
    return result

def insert(file, key, value):
    init(file)
    data = get_all(file)
    data[key] = value
    f = open(f'{file}.json', 'w')
    json.dump(data, f)
    f.close()
