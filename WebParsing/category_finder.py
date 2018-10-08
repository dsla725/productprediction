import requests
from bs4 import BeautifulSoup
from WebParsing import perekrestorparsing


def is_big(s):
    return s == s.upper()


html_parser = 'html.parser'


def search_in_items(res_search):
    i = 0
    item_categories = dict()
    for link in res_search.select('.xf-product-picture__link'):
        item_request = requests.get('https://www.perekrestok.ru/catalog' + link.get('href'))
        bs_item_request = BeautifulSoup(item_request.text, html_parser)
        res_item_request = bs_item_request.select('.xf-breadcrumbs__link')
        if len(res_item_request) > 0:
            this_category = res_item_request[len(res_item_request) - 1].text
            if this_category in item_categories:
                item_categories.update({this_category: item_categories[this_category] + 1})
            else:
                item_categories.update({this_category: 1})
        i += 1
        if i >= 5:
            break
    fmax = 0
    toresult = ''
    for fcategory in item_categories:
        c = item_categories[fcategory]
        if fmax < c:
            fmax = c
            toresult = fcategory
    return toresult


def search_in_categories(categories_list):
    bs_cat_list = BeautifulSoup(str(categories_list[0]), html_parser)
    max_count = 0
    result = ''
    for category in bs_cat_list.select('.xf-filter__checkbox-inner'):
        bs_count_list = BeautifulSoup(str(category), html_parser)
        count = int(bs_count_list.select('.xf-filter__item-count')[0].text)
        if max_count < count:
            max_count = count
            result = perekrestorparsing.delete_spaces(category.text).replace(str(count), '')
    return result


def search_by_small(naming):
    result = dict()
    for i in range(2, len(naming)):
        if len(naming[i]) >= 3:
            req = requests.get('https://www.perekrestok.ru/catalog/search', params={'text': naming[i]})
            res_search = BeautifulSoup(req.text, html_parser)

            if len(res_search.select('.xf-empty-section')) == 1:
                continue

            categories_list = res_search.select('[data-id|=category]')
            if len(categories_list) == 0:
                searching_res = search_in_items(res_search)
                if searching_res in result:
                    result.update({searching_res: result[searching_res] + 1})
                else:
                    result.update({searching_res: 1})
                continue

            searching_res = search_in_categories(categories_list)
            if searching_res in result:
                result.update({searching_res: result[searching_res] + 1})
            else:
                result.update({searching_res: 1})
    fmax = 0
    toresult = ''
    for fcategory in result:
        c = result[fcategory]
        if fmax < c:
            fmax = c
            toresult = fcategory
    return toresult


def find_category(shopping_list):
    for item in shopping_list:
        name = item.replace('.', ' ').replace('/', ' ').split()
        text_for_request = ''
        for i in range(2, len(name)):
            if is_big(name[i]):
                text_for_request += name[i] + ' '
        print(item)

        if len(text_for_request.split()) == 0:
            print(search_by_small(name))
            continue

        req = requests.get('https://www.perekrestok.ru/catalog/search', params={'text': text_for_request})
        res_search = BeautifulSoup(req.text, html_parser)

        if len(res_search.select('.xf-empty-section')) == 1:
            print(search_by_small(name))
            continue

        categories_list = res_search.select('[data-id|=category]')
        if len(categories_list) == 0:
            print(search_in_items(res_search))
            continue

        print(search_in_categories(categories_list))
