from requests import request
import json


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

    def find_bin_number(self, bin_number: str):
        load_dict = self._load_dict[str(bin_number)]
        bin_numbers = BinNumbers(load_dict=load_dict)
        bin_numbers.isBusinessCard = bool(load_dict['isBusinessCard'])

        bin_numbers.cardType = str(load_dict['cardType'])
        if bin_numbers.cardType == 'C':
            bin_numbers.cardType = 'Credit Card'
        elif bin_numbers.cardType == 'P' or bin_numbers.cardType == 'D' or bin_numbers.cardType == 'X':
            bin_numbers.cardType = 'Debit Card'

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


def seperate_dictionary(real_data):
    a = 1
    data_list = dict()
    load_dict = dict()

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

    for a in data_list:
        inner_dict = dict()
        for b in data_list[a]:
            inner_dict[str(b[0]).replace(" ", "")] = b[1]
        load_dict[str(a)] = inner_dict

    return load_dict


def get_bank_list(bin_number_list):
    # todo Card Type D, P = Debit C = Credit Card
    bank_list = {}
    for _ in bin_number_list:
        _bank_name = str(_.bankName).upper()
        empty_dict = dict()
        empty_dict['isBusinessCard'] = _.isBusinessCard
        empty_dict['cardType'] = _.cardType
        if empty_dict['cardType'] == 'C':
            empty_dict['cardType'] = 'Credit Card'
        elif empty_dict['cardType'] == 'P' or empty_dict['cardType'] == 'D' or empty_dict['cardType'] == 'X':
            empty_dict['cardType'] = 'Debit Card'
        empty_dict['bankName'] = _.bankName
        empty_dict['eftCode'] = _.eftCode
        empty_dict['brand'] = _.brand
        empty_dict['network'] = _.network

        if _bank_name not in bank_list:
            bank_list[_bank_name] = empty_dict
    return bank_list


def all_bin_numbers_to_list(load_dict):
    bin_number_list = []
    bin_numbers = BinNumbers(load_dict=load_dict)
    for _ in load_dict:
        bin_number = bin_numbers.find_bin_number(_)
        bin_number_list.append(bin_number)
    return bin_number_list


def get_request_from_url(request_url: str) -> dict:
    get_bin_numbers = request(method='Get', url=request_url)  # get bin numbers from url request
    request_json = get_bin_numbers.json()  # Get .json result
    return request_json['result']


def get_realm_data(request_result):
    realm_data = json.dumps(request_result, ensure_ascii=False)  # Check for Turkish charset in keyboard
    realm_data = realm_data.strip(' ] ').strip('[ ').split('},')  # Split data string to listable object
    return realm_data


def get_bin_number_list(url: str):
    request_result = get_request_from_url(request_url=url)  # Get result of .json only
    realm_data = get_realm_data(request_result=request_result)   # Get request and pull out results from dictionary
    loaded_dict = seperate_dictionary(real_data=realm_data)  # Get whole dictionary into load object
    bin_number_list_all = all_bin_numbers_to_list(load_dict=loaded_dict)  # Append items into list then loop over
    return bin_number_list_all, loaded_dict


# todo Card Type D, P = Debit C = Credit Card
url = 'https://ppgpayment-test.birlesikodeme.com:20000/api/ppg/Payment/BinList'
bin_number_list_all, loaded_dict = get_bin_number_list(url=url)   # Get bin_number_list_all and loaded_dict
bank_list = get_bank_list(bin_number_list_all)      # Get bank_list

a_list = list(print(_) for _ in bin_number_list_all)    # print items in Bin Number list
b_list = list(print(a, ' : ', b) for a, b in bank_list.items())    # print items in Bank list
print('Length of banks :', len(bank_list))   # Total Bank Count

