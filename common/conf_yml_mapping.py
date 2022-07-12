# -*- coding: UTF-8 -*- 
# 设置utf-8  显示中文
"""
@Create Time: 2022/6/27 15:00
@Author: guozg
@File：conf_yml_mapping.py
"""


class ConfYmlMapping():
    """
    config.yml 的映射
    """

    def __init__(self):
        # dir_conf 模块的key
        self.__dir_conf_key = "dir_conf"
        self.__case_key = "case"
        self.__caseyml_key = "caseyml"
        self.__common_key = "common"
        self.__config_key = "config"
        self.__report_tmp_key = "report_tmp"
        self.__report_key = "report"
        self.__request_dat_key = "requestdata"
        self.__response_data_key = "responsedata"
        self.__runlog_key = "runlog"
        # http_conf 模块的key
        self.__http_conf_key = "http_conf"
        self.__procotol_key = "procotol"
        self.__host_key = "host"
        self.__useragent_key = "useragent"

    # ****************dir_conf模块*******************
    def get_dir_conf_key(self):
        """返回config.yml中dir_conf的key值"""
        return self.__dir_conf_key

    def get_case_key(self):
        return self.__case_key

    def get_caseyml_key(self):
        return self.__caseyml_key

    def get_common_key(self):
        return self.__common_key

    def get_config_key(self):
        return self.__config_key

    def get_report_tmp_key(self):
        return self.__report_tmp_key

    def get_report_key(self):
        return self.__report_key

    def get_requestdata_key(self):
        return self.__request_dat_key

    def get_responsedata_key(self):
        return self.__response_data_key

    def get_runlog_key(self):
        return self.__runlog_key

    # ********************* http_conf 模块 *******************
    def get_http_conf_key(self):
        return self.__http_conf_key

    def get_procotol_key(self):
        return self.__procotol_key

    def get_host_key(self):
        return self.__host_key

    def get_useragent_key(self):
        return self.__useragent_key

