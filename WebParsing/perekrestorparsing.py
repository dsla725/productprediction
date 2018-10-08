import requests
import bs4

s = requests.get('https://www.perekrestok.ru')
# print(s.text)
b = bs4.BeautifulSoup(s.text, 'html.parser')
res = b.select('.xf-catalog-popup__item')
# c = bs4.BeautifulSoup(res, 'html.parser')

for item in res:
    print(item.getText)
    temp = bs4.BeautifulSoup(item.getText, 'html.parser')
    print(temp.text)
    # r = temp.select('.xf-catalog-popup__link  xf-ripple xf-ripple_gray js-xf-ripple js-catalog-popup__first-lvl-link js-catalog-popup__lvl-link js-lm__link')
    # print(r)
    # print('\n\ntest\n\n')
