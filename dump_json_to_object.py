import json

path = 'bin-number.json'

# Loading a JSON File to a Python Dictionary
with open(file='bin-number.json', encoding='utf-8') as file:
    data = json.load(file)
    json_data = dict()
    a = 1
    for results in data['result']:
        real_data = json.dumps(results, ensure_ascii=False).encode('utf-8')
        json_data[str(a)] = real_data.decode('utf-8')
        a += 1
for index, value in json_data.items():
    print(index, value)
