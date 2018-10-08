import requests
from bs4 import BeautifulSoup


def products_parsing(s):
    s = s.replace('<!-- /Products -->', '<!-- Products -->')
    return s.split('<!-- Products -->')[1]


def check_parsing(headers):
    html_parser = 'html.parser'
    url = 'https://check.ofd.ru/Document/FetchReceiptFromFns'
    site = requests.post(url, data=headers)
    res = products_parsing(site.text)
    bs_parser = BeautifulSoup(res, html_parser)
    products_list = bs_parser.select('.text-left')
    result_list = list()
    for item in products_list:
        result_list.append(item.text)
    print(result_list)


def parse_check(check):
    arguments = check.split('&')
    result = dict()
    for item in arguments:
        if 't=' in item:
            temp = item.split('=')[1]
            result.update(
                {'DocDateTime': temp[:4] + '-' + temp[4:6] + '-' + temp[6:11] + ':' + temp[11:13] + ':00.000Z'})
        elif 's=' in item:
            temp = item.split('=')[1]
            result.update({'TotalSum': int(temp.replace('.', ''))})
        elif 'fn=' in item:
            result.update({'FnNumber': item[3:]})
        elif 'i=' in item:
            result.update({'DocNumber': item[2:]})
        elif 'fp=' in item:
            result.update({'DocFiscalSign': item[3:]})
        elif 'n=' in item:
            result.update({'ReceiptOperationType': item[2:]})
    return result


check_dict = parse_check('t=20181007T222800&s=1491.00&fn=8712000101109913&i=1714&fp=3297358716&n=1')
check_parsing(check_dict)
