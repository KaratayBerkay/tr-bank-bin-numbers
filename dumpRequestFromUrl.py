from requests import request
import json


get_bin_numbers = request(method='Get', url='https://ppgpayment-test.birlesikodeme.com:20000/api/ppg/Payment/BinList')
request_json = get_bin_numbers.json()
request_result = request_json['result']
real_data = json.dumps(request_result, indent=2, ensure_ascii=False)
real_data = real_data.strip(' ] ').strip('[ ')

print(real_data)
