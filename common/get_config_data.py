# -*- coding: UTF-8 -*- 
# 设置utf-8  显示中文
"""
@Create Time: 2022/6/27 15:38
@Author: guozg
@File：get_config_data.py
"""
import os,yaml
from threading import RLock

cur_path = os.path.dirname(os.path.realpath(__file__))
proj_path = os.path.dirname(cur_path)

from common.conf_yml_mapping import ConfYmlMapping

class GetConfData():
    '''
    获取配置文件数据，对各自的路径进行拼接。
    '''
    __instance_lock = RLock()
    __instance = None

    def __new__(cls, *args, **kwargs):
        raise ImportError("不允许进行实例化")

    @classmethod
    def get_instance(cls):
        with cls.__instance_lock:
            if cls.__instance == None:
                cls.__instance = super().__new__(cls)

        cls.__instance.__init()
        return cls.__instance

    def __init(self):
        self.__mapping = ConfYmlMapping()
        self.__yml = "config/config.yml"
        self.__conf_yml_fp = os.path.join(proj_path,self.__yml)
        # 获取config.yml文件的中内容
        self.__conf_yml_data = self.get_conf_yml_data()
        # 获取dir_conf key对应的数据
        self.__dirconf_dict = self.get_dirconf_data()
        # 获取http_conf key 对应的数据
        self.__httpconf_dict = self.get_httpconf_data()


    def get_conf_yml_data(self) -> dict:
        '''获取config.yml文件的内容'''
        return yaml.safe_load(open(self.__conf_yml_fp,'r',encoding='utf-8'))

    # ****************** dir_conf 模块的数据 **************************
    def get_dirconf_data(self)->dict:
        '''获取dir_conf 相关的数据'''
        data = self.__conf_yml_data
        key = self.__mapping.get_dir_conf_key()
        return data.get(key)

    def get_case_dir_path(self):
        '''获取case目录路径'''
        key = self.__mapping.get_case_key()
        data = self.__dirconf_dict
        return os.path.join(proj_path,data.get(key))

    def get_caseyml_dir_path(self):
        '''获取caseyml目录路径'''
        key = self.__mapping.get_caseyml_key()
        data = self.__dirconf_dict
        return os.path.join(proj_path,data.get(key))

    def get_common_dir_path(self):
        '''获取common目录路径'''
        key = self.__mapping.get_common_key()
        data = self.__dirconf_dict
        return os.path.join(proj_path,data.get(key))

    def get_config_dir_path(self):
        '''获取config目录路径'''
        key = self.__mapping.get_config_key()
        data = self.__dirconf_dict
        return os.path.join(proj_path,data.get(key))

    def get_reporttmp_dir_path(self):
        '''获取临时report目录路径'''
        key = self.__mapping.get_report_tmp_key()
        data = self.__dirconf_dict
        return os.path.join(proj_path,data.get(key))

    def get_report_dir_path(self):
        '''获取report目录路径'''
        key = self.__mapping.get_report_key()
        data = self.__dirconf_dict
        return os.path.join(proj_path,data.get(key))

    def get_requestdata_dir_path(self):
        '''获取requestdata目录路径'''
        key = self.__mapping.get_requestdata_key()
        data = self.__dirconf_dict
        return os.path.join(proj_path,data.get(key))

    def get_responsedata_dir_path(self):
        '''获取responsedata目录路径'''
        key = self.__mapping.get_responsedata_key()
        data = self.__dirconf_dict
        return os.path.join(proj_path,data.get(key))

    def get_runlog_dir_path(self):
        '''获取runlog目录路径'''
        key = self.__mapping.get_runlog_key()
        data = self.__dirconf_dict
        return os.path.join(proj_path,data.get(key))

    # ****************** http_conf 模块的数据 **************************
    def get_httpconf_data(self)->dict:
        key = self.__mapping.get_http_conf_key()
        data = self.__conf_yml_data
        return data.get(key)

    def get_procotol(self):
        key = self.__mapping.get_procotol_key()
        data = self.__httpconf_dict
        return data.get(key)

    def get_host(self):
        key = self.__mapping.get_host_key()
        data = self.__httpconf_dict
        return data.get(key)

    def get_useragent(self):
        key = self.__mapping.get_useragent_key()
        data = self.__httpconf_dict
        return data.get(key)



if __name__ == "__main__":
    data = GetConfData()
    print(f"\n{'*' * 16} dir_conf 模块 {'*' * 16}")
    print(data.get_conf_yml_data())
    print(data.get_dirconf_data())
    print(data.get_case_dir_path())
    print(data.get_caseyml_dir_path())
    print(data.get_common_dir_path())
    print(data.get_config_dir_path())
    print(data.get_reporttmp_dir_path(),os.path.exists(data.get_reporttmp_dir_path()))
    print(data.get_report_dir_path())
    print(data.get_requestdata_dir_path())
    print(data.get_responsedata_dir_path())
    print(data.get_runlog_dir_path())
    print(f"\n{'*'*16} http_conf 模块 {'*'*16}")
    print(data.get_httpconf_data())
    print(data.get_procotol())
    print(data.get_host())
    print(data.get_useragent())





