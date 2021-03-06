import Database.Interaction as interact


def list_to_sqlarray(lst, delete_quote=False):
    string = str(lst).replace('[', '').replace(']', '')

    if delete_quote:
        string = string.replace("'", '')
    return string


class Table:

    def __init__(self, name):
        self.name = name
        self.columns = {}

    def add_column(self, name=None, type=None):

        if type is None:
            assert 0, "Impossible define type column"
        if name is None:
            assert 0, "Impossible define name column"

        self.columns.update({name: type})

        query = "ALTER TABLE {table_name} ADD {column_name} {column_type}".format(table_name=self.name,
                                                                                  column_name=name, column_type=type)
        return interact.execute(query)

    def clear_table(self):
        return interact.execute("DROP TABLE {name}".format(name=self.name))

    def count(self):
        return interact.execute("SELECT COUNT(*) FROM {table}".format(table=self.name))

    def get_info_by_id(self, id, names):
        query = "SELECT {names} FROM {table} WHERE id like '{id}'".format(table=self.name, id=id,
                                                                                    names=list_to_sqlarray(names, True))
        return interact.execute(query)

    def get_info_by_name(self, name, rows):
        query = "SELECT {names} FROM {table} WHERE name like '{name}'".format(table=self.name, name=name,
                                                                              names=list_to_sqlarray(rows, True))
        return interact.execute(query)

    def create_table(self, columns):
        interact.execute("CREATE TABLE {name} (CREATE_TIME text)".format(name=self.name))
        self.columns = columns
        for name in columns:
            type = columns[name]
            if type is None:
                continue
            self.add_column(name, type)

    def insert_into(self, fields):
        names = list()
        values = list()
        for name in fields.keys():
            value = fields[name]
            if value is None:
                continue
            names.append(name)
            values.append(value)

        query = "INSERT INTO {table_name} ({names}) VALUES({values})".format(table_name=self.name,
                                                                             names=list_to_sqlarray(names, True),
                                                                             values=list_to_sqlarray(values))
        return interact.execute(query)

    def delete_info_by_name(self, name):
        query = "DELETE FROM {table} WHERE name like '{name}'".format(table=self.name,name=name)
        return interact.execute(query)

    def delete_info_by_user_id(self, user_id):
        query = "DELETE FROM {table} WHERE user_id like '{user_id}'".format(table=self.name, user_id=user_id)
        return interact.execute(query)

    def select(self, names):
        if len(names) == 0:
            query = "SELECT {names} FROM {table}".format(names='*', table=self.name)
        else:
            query = "SELECT {names} FROM {table}".format(names=list_to_sqlarray(names, True), table=self.name)
        return interact.execute(query)

    def update_by_user_id(self, fields, user_id):
        names = fields.keys()
        query = "UPDATE {table_name} SET {changes} WHERE user_id like '{user_id}'"
        changes = ''
        i = 0
        for name in names:
            value = fields[name]
            if value is None:
                continue
            if i > 0:
                changes += ", {name} = '{value}'".format(name=name, value=value)
            else:
                changes += "{name} = '{value}'".format(name=name, value=value)
            i += 1

        query = query.format(table_name=self.name, user_id=user_id, changes=changes)
        return interact.execute(query)
