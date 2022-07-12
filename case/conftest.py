# -*- coding: UTF-8 -*- 
# 设置utf-8  显示中文
"""
@Create Time: 2022-6-29 15:17
@Author: test
@File：conftest.py.py
"""
import pytest
from common.get_config_data import GetConfData
from common.online_data import OnlineData
# from common.online_confdata import ConfData

@pytest.fixture(scope='session',autouse=True)
def get_confdata()->object:
    confdata = GetConfData()
    return confdata


@pytest.fixture(scope='session',autouse=True)
def get_online_obj()->object:
    online_data = OnlineData
    return online_data


# @pytest.fixture(scope='session',autouse=True)
# def get_online_confdata()->object:
#     data = GetConfData()
#     online_confdata = ConfData
#     setattr(online_confdata,'confdata',data)
#     return online_confdata


