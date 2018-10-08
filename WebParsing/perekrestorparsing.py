import requests
from bs4 import BeautifulSoup


def delete_spaces(s):
    return ' '.join(s.split())


def get_list():
    html_parser = 'html.parser'

    to_return = dict()
    site = requests.get('https://www.perekrestok.ru')
    biggest_list = BeautifulSoup(site.text, html_parser)
    res_biggest_list = biggest_list.select('.js-catalog-popup__lvl-item')

    for item_biggest_list in res_biggest_list:
        category = BeautifulSoup(str(item_biggest_list), html_parser)
        res_category = category.select('.js-catalog-popup__first-lvl-link')

        name = BeautifulSoup(str(res_category), html_parser)
        res_name = name.select('.xf-menu__item-text')[0]

        to_put = list()
        res_sublist = category.select('.js-catalog-popup__second-lvl-item')
        for item_sublist in res_sublist:
            sub_name = BeautifulSoup(str(item_sublist), html_parser)
            res_sub_name = sub_name.select('.xf-menu__item-text')[0]
            to_put.append(delete_spaces(res_sub_name.text))

        to_return.update({delete_spaces(res_name.text): to_put})

    return to_return
