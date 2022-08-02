# -*- coding: UTF-8 -*-
# 设置utf-8  显示中文
"""
@Create Time: 2022-6-27 11:58
@Author: test
@File：testdemo.py.py
"""
import pytest
import allure
from common.get_caseyml_data import get_ymlfile_data
from common.get_request_params import get_params
from common.api_base import ApiBase

ymldata,feature = get_ymlfile_data()

class TestDemo_resources_list():
    def setup(self):
        if feature and feature!="":
            allure.dynamic.feature(feature)

    @pytest.mark.parametrize("req_params,desc,asert,resp,depend,run,story",get_params(ymldata,'list'))
    def test_list(self,req_params,desc,asert,resp,depend,run,story):
        api_base = ApiBase.get_instance(req_params,desc,asert,resp,depend,run,story)
        api_base.run_case()

    @pytest.mark.parametrize("req_params,desc,asert,resp,depend,run,story", get_params(ymldata, 'category'))
    def test_category(self, req_params, desc, asert, resp, depend, run, story):
        api_base = ApiBase.get_instance(req_params, desc, asert, resp, depend, run, story)
        api_base.run_case()

    @pytest.mark.parametrize("req_params,desc,asert,resp,depend,run,story", get_params(ymldata, 'detail'))
    def test_detail(self, req_params, desc, asert, resp, depend, run, story):
        api_base = ApiBase.get_instance(req_params, desc, asert, resp, depend, run, story)
        api_base.run_case()

    @pytest.mark.parametrize("req_params,desc,asert,resp,depend,run,story", get_params(ymldata, 'recommend'))
    def test_recommend(self, req_params, desc, asert, resp, depend, run, story):
        api_base = ApiBase.get_instance(req_params, desc, asert, resp, depend, run, story)
        api_base.run_case()




