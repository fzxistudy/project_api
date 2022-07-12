# -*- coding: UTF-8 -*- 
# 设置utf-8  显示中文
"""
@Create Time: 2022/6/30 14:33
@Author: guozg
@File：handle_depend_data.py
"""
from string import Template
import simplejson
from jsonpath import jsonpath
from common.online_data import OnlineData
# from common.get_config_data import GetConfData
from common.get_json_filepath import get_json_filepath

# def handle_depend_data(request_param:dict,depend_data:dict,conf_data:GetConfData=None,online_data:object=None)->dict:
def handle_depend_data(request_param:dict,depend_data:dict,conf_data,online_data:object=None)->dict:
    '''
    处理依赖数据，返回处理后的请求数据。
    :param request_param: 请求参数
    :param depend_data: 依赖数据
    :param conf_data: config.yml 的数据，暂时不做处理
    :param online_data: 临时的在线数据数据class类
    :return:
    '''
    '''
    1：host的判断
    暂时不进行host是否与jenkins 及 config.yml文件中的host 一致相关的判断。
    后续确认相关的功能模块的host是否一致后再进行。
    2：online_data 
    暂时使用OnlineData class对象进行传递
    '''

    casedata = request_param
    # 当没有需要处理的依赖数据时
    if depend_data == None:
        return casedata
    # 有依赖数据
    else:
        # 对请求参数体进行转化为str,方便后续进行模板替换
        casedata_str = simplejson.dumps(casedata, indent=4, ensure_ascii=False, encoding='utf-8')
        depend_data_tmp = {}

        online = depend_data['online']

        # 判断数据的依赖方式是否为在线依赖。
        if online != False:
            # 当为在线的数据依赖时,case_id 不用填写，因为都使用统一的classin类 OnlineData
            # 获取依赖的数据对应的key值,注意此时yml文件中的值为list
            depend_key_list = depend_data['depend_key']
            # 获取要对哪个key所对应的值进行替换,注意此时yml文件中的值为list
            replace_key_list = depend_data['replace_key']
            for i in range(len(depend_key_list)):
                # 将值和key存入临时字典中，方便后续的模板替换
                depend_data_tmp[replace_key_list[i]] = getattr(OnlineData, depend_key_list[i])

        # 表示所依赖的数据存于json/yml文件中。
        else:
            # 获取类型
            type_str = depend_data['type']
            # 当数据依赖为response响应结果的json时
            if type_str == "response":
                # 此时的case_id 表示着json文件(含名称及路径)
                case_id:str = depend_data['case_id']
                # 获取依赖的数据在json文件中对应的哪个key,注意此时yml文件中的值为list
                depend_key_list = depend_data['depend_key']
                # 获取想要替换的请求数据所对应的哪个key,注意此时yml文件中的值为list
                replace_key_list = depend_data['replace_key']
                """
                1：case_id 需要进行判断是否为.json结尾，同时还要进行路径拼接
                2：在进行路径拼接的时候，要注意 case_id的开头，是否以"/" 或 "\\" 开头
                """
                # 调用公共函数,对case_id的值进行校验和拼接
                case_id = get_json_filepath(case_id,conf_data)

                # 读取文件
                with open(case_id, 'r', encoding='utf8') as fp:
                    # 对读取的数据进行转化为dict
                    fp_data = simplejson.loads(fp.read(), encoding='utf-8')

                # 使用jsonpath提取器，依次对数据进行提取，并存入到临时字典中
                for i in range(len(depend_key_list)):
                    depend_data_tmp[replace_key_list[i]] = jsonpath(fp_data, depend_key_list[i])[0]

            # request 类型的依赖后续处理，这块的处理相对难度高，临时有简易处理办法。
            elif type_str == "request":
                pass
        # 进行数据替换
        casedata_tmp = Template(casedata_str).safe_substitute(**depend_data_tmp)
        # 再转化为字典
        casedata = simplejson.loads(casedata_tmp, encoding='utf8')
        return casedata
