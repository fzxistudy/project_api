# -*- coding: UTF-8 -*- 
# 设置utf-8  显示中文
"""
@Create Time: 2022/6/27 16:32
@Author: guozg
@File：api_all_pub_pkg.py
@Description: case中所依赖的公共包
"""
import pytest
import yaml
import allure
import requests
import simplejson
from jsonpath import jsonpath
from string import Template
from urllib import parse
import os

from common.online_data import OnlineData
