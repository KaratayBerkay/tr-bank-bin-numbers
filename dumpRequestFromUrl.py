from requests import request
import json

url = 'https://ppgpayment-test.birlesikodeme.com:20000/api/ppg/Payment/BinList'
get_bin_numbers = request(method='Get', url=url)
request_json = get_bin_numbers.json()
request_result = request_json['result']
real_data = json.dumps(request_result, ensure_ascii=False)
real_data = real_data.strip(' ] ').strip('[ ').split('},')
data_list = dict()


class BinNumbers:
    isBusinessCard: bool
    cardType: str
    bankName: str
    prefixNo: int
    eftCode: str
    brand: str
    avoidPreauthInstall: bool
    avoidAuthInstall: bool
    network: str
    brandName: str
    responseCode: bool
    responseMessage: bool

    def __init__(self, load_dict):
        self._load_dict = load_dict

    def __repr__(self):
        return '****\nisBusinessCard: {0}\ncardType: {1}\nbankName: {2}\nprefixNo: {3}\neftCode: {4}\nbrand: {5}' \
               '\navoidPreauthInstall: {6}\navoidAuthInstall: {7}\nnetwork: {8}\nbrandName: {9}\nresponseCode: ' \
               '{10}\nresponseMessage: {11}\n-----------------'.format(
                self.isBusinessCard, self.cardType, self.bankName, self.prefixNo, self.eftCode, self.brand,
                self.avoidPreauthInstall, self.avoidAuthInstall, self.network, self.brandName, self.responseCode,
                self.responseMessage)

    def give_all_bin_numbers(self):
        for _ in sorted(self._load_dict):
            print(_, '-*********************************************')
            for a, b in self._load_dict[_].items():
                print(a, b)

    def find_binumber(self, bin_bumber: str):
        load_dict = seperate_dictionary()
        load_dict = load_dict[str(bin_bumber)]
        bin_numbers = BinNumbers(load_dict=load_dict)
        bin_numbers.isBusinessCard = bool(load_dict['isBusinessCard'])
        bin_numbers.cardType = str(load_dict['cardType'])
        bin_numbers.bankName = str(load_dict['bankName'])
        bin_numbers.prefixNo = str(load_dict['prefixNo'])
        bin_numbers.eftCode = str(load_dict['eftCode'])
        bin_numbers.brand = str(load_dict['brand'])
        bin_numbers.avoidPreauthInstall = bool(load_dict['avoidPreauthInstall'])
        bin_numbers.avoidAuthInstall = bool(load_dict['avoidAuthInstall'])
        bin_numbers.network = str(load_dict['network'])
        bin_numbers.brandName = bool(load_dict['brandName'])
        bin_numbers.responseCode = bool(load_dict['responseCode'])
        bin_numbers.responseMessage = bool(load_dict['responseMessage'])
        return bin_numbers


def seperate_dictionary():
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

    for a in data_list:
        inner_dict = dict()
        for b in data_list[a]:
            inner_dict[str(b[0]).replace(" ", "")] = b[1]
        load_dict[str(a)] = inner_dict

    return load_dict


load_dict = seperate_dictionary()   # Get whole dictionary into load object
bin_numbers = BinNumbers(load_dict=load_dict)   # Get BinNumbers into numbers

bin_number_list = []   # Append items into list then loop over
for _ in load_dict:
    bin_number = bin_numbers.find_binumber(_)
    bin_number_list.append(bin_number)

# See items in list
for _ in bin_number_list:
    print(_)


