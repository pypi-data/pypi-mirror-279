def 网页协议_获取_响应文本(响应对象):
    """
    获取响应的文本内容
    :param 响应对象: 服务器响应对象
    :return: 响应的文本内容，如果响应为 None 或出现任何异常则返回空字符串
    """
    try:
        if 响应对象 is not None:
            return 响应对象.text
        else:
            return ''
    except Exception:
        return ''