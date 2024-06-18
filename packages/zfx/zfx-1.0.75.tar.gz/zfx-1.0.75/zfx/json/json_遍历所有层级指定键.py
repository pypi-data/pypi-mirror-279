import jsonpath


def json_遍历所有层级指定键(数据对象, 键名):
    """
    使用 遍历所有层级下指定键的值，逐层进行寻找。

    参数:
    数据对象 (dict): 数据对象（字典），而不是字符串。
    键名 (str): 要查找的键名。

    返回:
    list: 包含所有匹配键值的列表，如果没有匹配或异常则返回空列表。
    """
    try:
        # 构建 JSONPath 表达式
        expr = f'$..{键名}'

        # 执行 JSONPath 查询
        匹配的值 = jsonpath.jsonpath(数据对象, expr)

        return 匹配的值 if 匹配的值 else []
    except Exception:
        return []