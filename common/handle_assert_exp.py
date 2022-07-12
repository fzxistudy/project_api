# -*- coding: UTF-8 -*- 
# 设置utf-8  显示中文
"""
@Create Time: 2022-7-4 11:19
@Author: test
@File：handle_assert_exp.py
"""
import re
import pytest
from jsonpath import jsonpath


def handle_assert_exp(request, assert_exps) -> str:
    '''
    处理断言表达式，将表达式转化为正确的方便查阅的结果  \n
    :param request: requests.request() request请求。
    :param assert_exps: 原始断言表达式。
    :return: 处理后的表达式,如pytest.assume(200== 200)。
    '''

    req = request
    req_json = None
    req_text = req.text
    try:
        req_json = req.json()
    except Exception as e:
        msg = f"在获取request的响应json结果时，发生了异常，信息为：{e}"
        pytest.fail(msg)
    # # 表达式中是否有[0]的标识
    # flag0=False
    # # 表达式中是否有状态码比较的标识
    # codeflag = False

    # 处理后的表达式
    exp_list = []

    # 判断断言表达式是否为列表，即一个case有多重断言
    if isinstance(assert_exps, list) and len(assert_exps) > 0:

        for asert_exp in assert_exps:
            exp_str = _extract_exp_content(req, asert_exp)
            exp_list.append(exp_str)

    else:
        exp_str = _extract_exp_content(req, assert_exps)
        exp_list.append(exp_str)

    return " , ".join(exp_list)


def _extract_exp_content(req, asert_exp) -> str:
    '''
    提取表达式中的内容
    :param req: request请求
    :param asert_exp: 断言表达式
    :return: 返回拼接好的，提取后的内容。
    '''
    req_text = req.text
    req_json = req.json()
    # 对标识重新赋值
    flag0 = False
    codeflag = False
    if "(jsonpath(" in asert_exp:
        # 提取表达式前半段内容
        exp_content_prefix = re.findall(r"pytest\.assume\((.+?)\(jsonpath", asert_exp)
        # 检测是否是[0]
        if "[0]" in asert_exp:
            # 提取表达式后半段内容，主要是jsonpath中的表达式内容
            exp_content_suffix = re.findall(r"\(jsonpath\((.+?)\)\[0\]\)\)", asert_exp)
            # 设置标识
            flag0 = True
        # 表示没有[0]
        else:
            # 提取jsonpath中的表达式内容
            exp_content_suffix = re.findall(r"\(jsonpath\((.+?)\)\)\)", asert_exp)

    elif "jsonpath(" in asert_exp:
        # 提取表达式的前半段内容
        exp_content_prefix = re.findall(r"pytest\.assume\((.+?)jsonpath", asert_exp)
        if "[0]" in asert_exp:
            # 提示jsonpath中的表达式内容
            exp_content_suffix = re.findall(r"jsonpath\((.+?)\)\[0\]\)", asert_exp)
            flag0 = True
        else:
            exp_content_suffix = re.findall(r"jsonpath\((.+?)\)\)", asert_exp)

    # 判断是否进行了状态码比较。
    elif "req.status_code" in asert_exp:
        codeflag = True
        exp_content_prefix = re.findall(r"pytest\.assume\((.+?)req\.status_code", asert_exp)

    # 当进行状态码比较时
    if codeflag:
        value = req.status_code

    elif flag0:
        value = jsonpath(*eval(exp_content_suffix[0]))[0]

    else:
        value = jsonpath(*eval(exp_content_suffix[0]))
    # 拼接表达式
    exp_str = f"pytest.assume({exp_content_prefix[0]} {value})"

    return exp_str


def handle_assert(request, asert_exps) -> None:
    '''
    处理断言  \n
    :param request: request请求
    :param asert_exps: 断言表达式
    :return: None
    '''
    req = request
    req_text = req.text
    req_json = req.json()
    if isinstance(asert_exps, list):
        for asert_exp in asert_exps:
            eval(asert_exp)
    else:
        eval(asert_exps)
