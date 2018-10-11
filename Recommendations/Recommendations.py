import Database.Table as Table
import datetime
from math import factorial, exp

products = Table.Table('products')
users = Table.Table('users')


def parse_date(date):
    arr = date.split('.')
    return datetime.date(arr[2], arr[1], arr[0])


def probability_puasson(alpha, num):
    return (exp(-alpha * num) * (alpha ** num)) / factorial(num)


class User:
    def __init__(self, id):
        self.id = id
        self.dates_products = {}
        self.get_dates_products()

    def get_dates_products(self):
        tickets = users.get_info_by_id(id=self.id, names=['tickets', 'date'])
        """
            id_user |             tickets               |   date
               id     id_prod id_prod id_prod id_prod     dd.mm.yy
        """
        for ticket in tickets:
            date = parse_date(ticket[1])
            ids_products = ticket[0].split(' ')
            for id in ids_products:
                if getattr(self.dates_products, id, None) is None:
                    self.dates_products[id].append(date)

    def average_frequency(self, id_product):
        dates = self.dates_products[id_product]
        lost_time = dates[-1] - dates[0]
        days = lost_time.year * 365 + lost_time.month * 30.5 + lost_time.day
        return len(dates) / days

    def probably_next_time_buy(self, id_product):
        average = self.average_frequency(id_product)
        day = 0
        while probability_puasson(average, day + 1) > probability_puasson(average, day):
            day = day + 1
        return day, probability_puasson(average, day)

    def probably_next_date(self, id_product):
        days, probability = self.probably_next_time_buy(id_product)
        delta = datetime.timedelta(days=days)
        return self.dates_products[-1][0] + delta, probability

    def get_top_recommendations(self, count):
        today = datetime.datetime.today()
        products_today = list()
        for id in self.dates_products:
            date, probability = self.probably_next_time_buy(id)
            if date == today:
                products_today.append((probability, id))

        answer = list()

        if len(products_today) < count:
            for product in products_today:
                answer.append(product[1])
            return answer
        products_today = sorted(products_today)
        for i in range(1, count + 1):
            answer.append(products_today[-i][1])
        return answer


def run():
    users_ids = users.select(['id'])
    for user_id in users_ids:
        id = user_id[0]
        print("id = ", id, "products_ids = ", User(id).get_top_recommendations(5))
