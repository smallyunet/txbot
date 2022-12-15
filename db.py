import json
import os

def get_all(file):
    if not os.path.isfile(f'{file}.json'):
        f = open(f'{file}.json', 'w')
        json.dump({}, f)
        f.close()
    f = open(f'{file}.json', 'r')
    data = json.load(f)
    f.close()
    return data

def get_latest(file, num=1):
    if not os.path.isfile(f'{file}.json'):
        f = open(f'{file}.json', 'w')
        json.dump({}, f)
        f.close()
    data = get_all(file)
    keys = list(data.keys())
    keys.sort()
    keys = keys[-num:]
    result = {}
    for key in keys:
        result[key] = data[key]
    return result

def insert(file, key, value):
    if not os.path.isfile(f'{file}.json'):
        f = open(f'{file}.json', 'w')
        json.dump({}, f)
        f.close()
    data = get_all(file)
    data[key] = value
    f = open(f'{file}.json', 'w')
    json.dump(data, f)
    f.close()
