# -*- coding: UTF-8 -*- 
# 设置utf-8  显示中文
"""
@Create Time: 2022/6/27 16:51
@Author: guozg
@File：api_base.py
"""
import inspect

from common.api_all_pub_pkg import *
from common.step_msg import step_msg
from common.handle_depend_data import handle_depend_data
from common.handle_response_data import handle_response_data
from common.handle_assert_exp import handle_assert_exp,handle_assert
from common.save_log import logger


class ApiBase():
    ''''''

    def __init__(self,req_params,desc,asert,resp,dependdata,run,stroy,confdata):
        '''
        初始化时需要传入的参数  \n
        :param req_params: 请求参数
        :param desc: 描述/每个case的目的，用于最终的case title
        :param asert: 断言
        :param resp: 响应结果的处理
        :param dependdata: 依赖的数据
        :param run: 是否运行
        :param stroy: 功能模块
        :param confdata: config.yml 数据
        '''
        self.__run = run
        if self.__run == False:
            pytest.skip(f"该用例的run的值为：{run} , 所以不需要执行！！！")

        self.__req_params = req_params
        self.__desc = desc
        self.__asert = asert
        self.__resp = resp
        self.__depend_data = dependdata
        self.__story = stroy
        self.__confdata = confdata

    def run_case(self):
        ''''''
        if self.__desc and self.__desc !="":
            # 设置报告中的case的title
            allure.dynamic.title(self.__desc)
        if self.__story and self.__story !="":
            # 设置报告的case的功能名称
            allure.dynamic.story(self.__story)
        # 设置报告中的描述
        allure.dynamic.description(f"""
        传入的请求参数：{self.__req_params}
        传入的依赖数据：{self.__depend_data}
        传入的响应结果动作：{self.__resp}
        传入的断言：{self.__asert}
        """)

        msg = f"第一步：处理数据依赖"
        req_params = handle_depend_data(self.__req_params,self.__depend_data,self.__confdata)
        step_msg(msg)

        msg = f"第二步：进行接口请求，参数为{req_params}"
        step_msg(msg)

        req = requests.request(**req_params)
        msg = f"第三步：获取到的接口响应结果：{req.json()}"
        step_msg(msg)

        msg = f"第四步：处理响应结果"
        handle_response_data(self.__resp,req.json(),self.__confdata)
        step_msg(msg)

        exp_str = handle_assert_exp(req,self.__asert)
        msg=f"第五步：处理断言. 原始表达式为: {self.__asert} ; 处理后的表达式为: {exp_str}"
        step_msg(msg)
        handle_assert(req,self.__asert)

    def run_case_havelog(self):
        ''''''
        base = inspect.stack()
        filename = base[1].filename
        filename = os.path.basename(filename)
        func_name = base[1].function
        line_no = base[1].lineno
        __log_fmt = f"{filename:<10s}:{line_no:0>3d}:{func_name:<10s}:"
        if self.__desc and self.__desc != "":
            # 设置报告中的case的title
            allure.dynamic.title(self.__desc)
        if self.__story and self.__story != "":
            # 设置报告的case的功能名称
            allure.dynamic.story(self.__story)
        # 设置报告中的描述
        allure.dynamic.description(f"""
        传入的请求参数：{self.__req_params}
        传入的依赖数据：{self.__depend_data}
        传入的响应结果动作：{self.__resp}
        传入的断言：{self.__asert}
        """)

        msg = f"第一步：处理数据依赖"
        req_params = handle_depend_data(self.__req_params, self.__depend_data, self.__confdata)
        logmsg = f"{__log_fmt}{msg}"
        logger.info(logmsg)
        step_msg(msg)

        msg = f"第二步：进行接口请求，参数为{req_params}"
        step_msg(msg)
        logmsg = f"{__log_fmt}{msg}"
        logger.info(logmsg)

        req = requests.request(**req_params)
        msg = f"第三步：获取到的接口响应结果：{req.json()}"
        step_msg(msg)
        logmsg = f"{__log_fmt}{msg}"
        logger.info(logmsg)

        msg = f"第四步：处理响应结果"
        handle_response_data(self.__resp, req.json(), self.__confdata)
        step_msg(msg)
        logmsg = f"{__log_fmt}{msg}"
        logger.info(logmsg)

        exp_str = handle_assert_exp(req, self.__asert)
        msg = f"第五步：处理断言. 原始表达式为: {self.__asert} ; 处理后的表达式为: {exp_str}"
        step_msg(msg)
        logmsg = f"{__log_fmt}{msg}"
        logger.info(logmsg)
        handle_assert(req, self.__asert)

