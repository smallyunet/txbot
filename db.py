import json

def get_all(file):
    f = open(f'{file}.json', 'r')
    data = json.load(f)
    f.close()
    return data

def get_latest(file, num=1):
    data = get_all(file)
    return list(data.values())[-num:]

def insert(file, key, value):
    data = get_all(file)
    data[key] = value
    f = open(f'{file}.json', 'w')
    json.dump(data, f)
    f.close()
