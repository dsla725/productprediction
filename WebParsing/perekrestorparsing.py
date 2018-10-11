import requests
from bs4 import BeautifulSoup
from Database.Table import Table


def delete_spaces(s):
    return ' '.join(s.split())


html_parser = 'html.parser'


def get_list():
    to_put = list()
    site = requests.get('https://www.perekrestok.ru')
    biggest_list = BeautifulSoup(site.text, html_parser)
    res_biggest_list = biggest_list.select('.js-catalog-popup__lvl-item')

    for item_biggest_list in res_biggest_list:
        category = BeautifulSoup(str(item_biggest_list), html_parser)
        res_sublist = category.select('.js-catalog-popup__second-lvl-item')
        for item_sublist in res_sublist:
            sub_name = BeautifulSoup(str(item_sublist), html_parser)
            res_sub_name = sub_name.select('.xf-catalog-popup__link')[0]
            to_put.append(delete_spaces(res_sub_name.get('href')))

    return to_put


def get_items_list(category_list):
    table = Table('products')
    for category in category_list:
        print(category)
        if '/brand' in category:
            continue
        site = requests.get('https://www.perekrestok.ru' + category)
        site_parser = BeautifulSoup(site.text, html_parser)
        category_name = site_parser.select('.xf-caption__title')[0].text
        items_to_dict = list()
        count = int(site_parser.select('.js-list-total__total-count')[0].text)
        if count != 0 and count % 24 == 0:
            count -= 1
        for i in range(1, int(count / 24) + 2):
            page = requests.get('https://www.perekrestok.ru' + category, params={'page': i})
            page_parser = BeautifulSoup(page.text, html_parser)
            catalog_parser = BeautifulSoup(str(page_parser.select('#catalogItems')[0]), html_parser)
            item_list = catalog_parser.select('.xf-product-title__link')
            for product in item_list:
                items_to_dict.append(delete_spaces(product.text))
        for item in items_to_dict:
            table.delete_info_by_name(item)
            table.insert_into({'category': category_name, 'name': item})

# get_items_list(get_list())
