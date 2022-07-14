# -*- coding: UTF-8 -*- 
# 设置utf-8  显示中文
"""
@Create Time: 2022/6/30 15:25
@Author: guozg
@File：handle_response_data.py
"""
from jsonpath import jsonpath
import simplejson

from common.online_data import OnlineData
from common.get_json_filepath import get_json_filepath

def handle_response_data(response_yml_data:list,response_json_data:dict,online_data:object=None)->None:
    '''
    处理响应结果。需要传入case 对应的yml文件中的response模块下的数据、request的请求响应json结果、config.yml 数据 \n
    :param response_yml_data: case对应的yml文件中的response模块下的数据
    :param response_json_data: request的请求响应json结果
    # :param conf_yml_data: config.yml 数据
    :param online_data: OnlineData class 暂时不用
    :return: None
    '''
    resp_yml = response_yml_data
    resp_json = response_json_data

    # 当response key 对应的值不为空时，表示需要处理响应结果。
    if resp_yml and resp_yml != "":
        #  获取filepath的值。
        fp = resp_yml['filepath']
        # 获取resp_keys 的值，即要提取的响应结果对应的哪些key值。为list
        save_data_list = [jsonpath(resp_json, item)[0] for item in resp_yml['resp_keys']]
        # 响应的结果要保存在json文件中的哪些key下。
        save_key = [item for item in resp_yml['keys']]

        # 做一次判断，是将数据保存到json文件中还是保存到类属性中
        if fp == "online":
            for i in range(len(save_key)):
                setattr(OnlineData, save_key[i], save_data_list[i])

        # 表示要将结果保存到json文件中
        else:
            # 此时要拼接json文件的路径。在拼接之前要校验是否以".json" 结尾 ，以及是否以 "\" 或 "/" 开头
            fp = get_json_filepath(fp)

            save_data = {save_key[i]: save_data_list[i] for i in range(len(save_key))}

            with open(f"{fp}", 'w', encoding='utf8') as fp:
                fp.write(simplejson.dumps(save_data, ensure_ascii=False, encoding='utf-8'))