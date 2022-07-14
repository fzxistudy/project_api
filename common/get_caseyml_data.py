# -*- coding: UTF-8 -*- 
# 设置utf-8  显示中文
"""
@Create Time: 2022/6/30 22:45
@Author: guozg
@File：get_caseyml_data.py
@Description: yml文件名要与 case所在的 py 文件名 保持一致。如test_login.py对应的yml文件名为test_login.yml
"""
import inspect
import os
import pytest
import yaml
from common.get_config_data import GetConfData

confdata = GetConfData.get_instance()

def get_ymlfile_data()->list:
    '''
    获取py文件对应的yml文件的数据,当yml文件不存在时，直接置为fail
    :return:
    '''
    base = inspect.stack()
    # 获取case所在的py文件名
    py_name = os.path.basename(base[1].filename)
    data = {}
    # 检测文件是否存在
    yml_fp = get_yml_fp(py_name,'.yml')
    if os.path.exists(yml_fp):
        # 获取文件数据
        data = yaml.safe_load(open(yml_fp,'r',encoding='utf-8'))
    # 表示文件不存在。此时有可能是文件的后缀为.yaml
    else:
        yaml_fp = get_yml_fp(py_name, '.yaml')
        if os.path.exists(yaml_fp):
            data = yaml.safe_load(open(yaml_fp,'r',encoding='utf-8'))

        else:

            pytest.fail(f"******请检测caseyml目录下是否符合规定的yml文件,请注意yml命名规则.******\n"
                        f"例：test_login.py对应的yml文件为：test_login.yml\n"
                        f"{yml_fp} 不存在\n"
                        f"{yaml_fp} 也不存在\n")

    return [data,data.get('feature')]

def get_yml_fp(pyname:str,suffix:str='.yml')->str:
    '''
    获取yml文件的路径(含名称)  \n
    :param suffix: 后缀
    :param pyname: case所在的py文件名
    :return: 拼接后的yml文件(含路径)
    '''
    if suffix == ".yaml":
        yml_name = f"{pyname.rstrip('.py')}.yaml"
    else:
        yml_name = f"{pyname.rstrip('.py')}.yml"
    # 获取caseyml的目录路径
    caseyml_dir = confdata.get_caseyml_dir_path()
    # 拼接文件路径
    yml_fp = os.path.join(caseyml_dir, yml_name)
    return yml_fp






