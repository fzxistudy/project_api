# -*- coding: UTF-8 -*- 
# 设置utf-8  显示中文
"""
@Create Time: 2022-6-28 20:11
@Author: test
@File：__init__.py.py
"""
import os,sys
# cur_path = os.path.dirname(__file__)
# 下面的代码是兼容低版本，如3.9（不含）以下的python编译器
cur_path = os.path.dirname(os.path.realpath(__file__))
proj_path = os.path.dirname(cur_path)
sys.path.append(proj_path)