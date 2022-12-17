from requests import request
import json

url = 'https://ppgpayment-test.birlesikodeme.com:20000/api/ppg/Payment/BinList'
get_bin_numbers = request(method='Get', url=url)
request_json = get_bin_numbers.json()
request_result = request_json['result']
real_data = json.dumps(request_result, ensure_ascii=False)
real_data = real_data.strip(' ] ').strip('[ ').split('},')
data_list = dict()
a = 1

for _ in real_data:
    object_string = _.replace('{', '').replace('}', '')
    object_string = object_string.replace('"', "").replace("'", "").split(',')
    split_list = list()
    prefix_name = ''
    for _ in object_string:
        item_key = _.split(': ')[0]
        item_value = _.split(': ')[1]
        if 'prefixno' in item_key.lower():
            prefix_name = item_value
        if str(item_value).replace("'", "") == 'false':
            item_value = False
        if str(item_value).replace("'", "") == 'true':
            item_value = True

        split_list.append([item_key, item_value])

    data_list[prefix_name] = list(split_list)
    a += 1

load_dict = dict()
inner_dict = dict()

for a in data_list:
    inner_dict = dict()
    for b in data_list[a]:
        inner_dict[str(b[0])] = b[1]
    load_dict[str(a)] = inner_dict

for _ in sorted(load_dict):
    print(_, ':', load_dict[_])
    for a, b in load_dict[_].items():
        print(a, b)

# print(load_dict['979300'])

