import Database.Interaction as interact


def get_name_product_as_list(all_string):
    all_string = all_string.lower()
    all_string = all_string.replace('%', '#')
    all_string = all_string.replace('.', ' ')
    return sorted(all_string.split(' '))


def get_product_id(all_name):
    name = get_name_product_as_list(all_name)
    query = "SELECT name, category FROM products WHERE name like '%{name_product}%'"
    result_query = list()
    num = -1
    for i in range(0, len(name)):
        query = query.format(name_product=name[0])
        result_query = interact.execute(query)
        if not len(result_query) == 0:
            num = i
            break
    if num < 0:
        return result_query
    for i in range(0, len(name)):
        if i == num:
            continue
        contain_cur = list()
        for element in result_query:
            if name[i] in element:
                contain_cur.append(element)
        if len(contain_cur) == 0:
            continue
        if len(contain_cur) == 1:
            return contain_cur
        result_query = contain_cur
    return result_query
