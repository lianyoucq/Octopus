# -*- coding:utf-8 -*-
from urllib import request

def unquote(url: str) -> str :
    if url is not None and isinstance(url, str):
        return  request.unquote(url)
    return url