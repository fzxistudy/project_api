# -*- coding: UTF-8 -*- 
# 设置utf-8  显示中文
"""
@Create Time: 2022-7-14 11:03
@Author: test
@File：get_datetime.py
"""

import datetime

class GetDateTime():

    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance == None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        fmt = "%Y_%m_%d"
        self.__curdate = datetime.date.today().strftime(fmt)

    def get_curdate(self)->str:
        return self.__curdate