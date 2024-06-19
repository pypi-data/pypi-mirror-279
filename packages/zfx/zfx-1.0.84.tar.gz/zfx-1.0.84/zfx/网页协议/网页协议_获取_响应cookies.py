def 网页协议_获取_响应cookies(响应对象):
    """
    获取响应的 cookies
    :param 响应对象: 服务器响应对象
    :return: 响应的 cookies，如果响应为 None 或出现任何异常则返回空字典
    """
    try:
        if 响应对象 is not None:
            return 响应对象.cookies
        else:
            return {}
    except Exception:
        return {}