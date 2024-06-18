import jsonpath


def json_遍历指定层级指定键(数据对象, 层级路径, 键名):
    """
    使用 遍历指定层级指定键，按照指定的目录下开始进行寻找,层级名称不固定可用*号代替。
    zfx.json_遍历指定层级指定键(result, "data.wickedProductNoCache.*.edges", "*.shortId")
    最终一定要定位到自己想要的键去。

    参数:
    数据对象 (dict): 包含数据的字典对象。
    层级路径 (str): JSONPath 表达式的路径部分。
    键名 (str): 要查找的键名。

    返回:
    list: 包含所有匹配键值的列表，如果没有匹配或异常则返回空列表。

    使用示例：
    结果 = json_遍历指定层级指定键(数据对象, 'data.第一层.第二层', '价格')
    """
    try:
        # 构建 JSONPath 表达式
        表达式 = f'$.{层级路径}[*].{键名}'

        # 执行 JSONPath 查询
        匹配的值 = jsonpath.jsonpath(数据对象, 表达式)

        return 匹配的值 if 匹配的值 else []
    except Exception:
        return []