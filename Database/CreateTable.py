from sqlite3 import OperationalError

import Database.Table as Table


def create():
    products = Table.Table('products')
    try:
        products.create_table({
            'category': 'text',
            'name': 'text'
        })
    except OperationalError:
        print('WARNING: Operational error while creating ProductTable')
