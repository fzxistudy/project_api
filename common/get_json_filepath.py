# -*- coding: UTF-8 -*- 
# 设置utf-8  显示中文
"""
@Create Time: 2022/6/30 20:52
@Author: guozg
@File：get_json_filepath.py
"""
import os.path
from common.get_config_data import GetConfData

def get_json_filepath(filepath:str)->str:
    '''
    获取数据依赖/response结果 的json文件的路径  \n
    :param filepath: yml文件中 response模块下的filepath的值 或 depend_on模块下的case_id 的值。
    # :param conf_data: config.yml的值
    :return: 拼接后的 json文件的路径。
    '''
    # 先进行检测是否以 ".json" 为结尾，再判断 是否以"\\" 或 "/"开头
    if not filepath.endswith(".json"):
        filepath = f"{filepath}.json"

    # 当以 \ 或 / 开头时，必须要去掉，否则拼接路径会失败。
    if filepath.startswith("\\"):
        filepath = filepath.lstrip("\\")
    elif filepath.startswith("/"):
        filepath = filepath.lstrip("/")

    # 进行路径拼接
    conf_data = GetConfData.get_instance()
    dir = conf_data.get_responsedata_dir_path()
    # 返回结果。
    return os.path.join(dir,filepath)
