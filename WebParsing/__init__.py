from Database import CreateTable
from Database.Table import Table

t = Table('products')
# t.clear_table()
# CreateTable.create()

# print(t.get_info_by_name('123', ['category', 'name']))
print(t.count())
