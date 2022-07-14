# -*- coding: UTF-8 -*- 
# 设置utf-8  显示中文
"""
@Create Time: 2022-6-29 15:17
@Author: test
@File：conftest.py.py
"""
import pytest
from common.online_data import OnlineData


@pytest.fixture(scope='session',autouse=True)
def get_online_obj()->object:
    online_data = OnlineData
    return online_data

