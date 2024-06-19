def 网页协议_获取_HTTP状态码(响应对象):
    """
    获取 HTTP 状态码
    :param 响应对象: 服务器响应对象
    :return: HTTP 状态码，如果响应为 None 或出现任何异常则返回 None
    """
    try:
        if 响应对象 is not None:
            return 响应对象.status_code
        else:
            return None
    except Exception:
        return None