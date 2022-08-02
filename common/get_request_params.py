# -*- coding: UTF-8 -*- 
# 设置utf-8  显示中文
"""
@Create Time: 2022-6-29 11:31
@Author: test
@File：get_request_params.py
"""
import pytest
from urllib import parse
import simplejson
from string import Template
# from common.get_config_data import GetConfData

class GetReqParams():
    '''获取接口请求相关的参数,最后会返回[[请求参数,case描述,断言,响应结果的处理,依赖的数据,是否运行,story模块]]'''

    def get_params(self,ymldata:dict,caseymlname:str)->list:
        '''
        需要传入yml文件的数据、case对应的yml文件中的key \n
        返回[[请求参数,case描述,断言,响应结果的处理,依赖的数据,是否运行,story模块],[……]……]
        :param ymldata:  yml文件的数据。
        :param caseymlname: case对应的yml文件中的key，如login
        :return: list[[req,desc,asert,resp,depend,run,story],[req,desc,asert,resp,depend,run,story],……]
        '''

        if isinstance(ymldata, dict) and len(ymldata) > 1:
            # self.__ymldata = ymldata
            pass
        else:
            pytest.fail(f"传入的的yml数据错误，内容为：{ymldata}")

        if isinstance(caseymlname, str) and caseymlname.strip() != "":
            # self.__casename = caseymlname.strip()
            caseymlname = caseymlname.strip()
        else:
            pytest.fail(f"传入的case对应的yml文件中的key的名字错误,值为：{caseymlname}")

        # if isinstance(confobj,GetConfData):
        #     self.__conf = confobj
        # else:
        #     pytest.fail(f"传入的confobj不是GetConfData对象,type为：{type(confobj)}")

        # 获取case对应的yaml数据
        casedata: dict = ymldata.get(caseymlname)
        path = casedata['path']
        # 全局procotol
        g_procotol = ymldata.get('procotol')
        # 全局host
        g_host = ymldata.get('host')
        # case 自己的host与procotol
        m_host = casedata.get('host')
        m_procotol = casedata.get('procotol')

        run = True
        story = ymldata.get('story')
        if ymldata.get('run') == False:
            run = False

        # 判断模块自己的host与procotol
        # 当模块自己的host为空或None时，使用全局的。暂不考虑使用全局进行替换
        host = m_host
        procotol = m_procotol
        if m_host == None or m_host == "":
            # 判断全局的host是否也为空
            if g_host == None or g_host == "":
                host = "$host"
            else:
                host = g_host

        if m_procotol == None or m_procotol == "":
            if g_procotol == None or g_procotol == "":
                procotol = "$procotol"
            else:
                procotol = g_procotol

        # if host==None or host == "":
        #     host="$host"
        #
        # if procotol == None or procotol == "":
        #     procotol = "$procotol"

        # 这里使用模板技术，方便从config.yml 文件中读取host和procotol进行替换。
        '''
        1：这里需要注意及确认的是：是每个模块的host 都是一样的，还是说不同的模块的host都不一样？需要找恩强确认
        2：从jenkins中获取到的host是在此时进行替换，还是在哪里进行替换
        3：从config.yml 中获取到的host该当怎样处理
        4：当不同模块的host 不一样时，方案如下：
            a：将所有的模块全部收集起来，目前有3个，不同模块的host 可以简写，如：V5的登录相关：v5_host,v6_host
            b：将这些host全部写在每个yaml和config.yml文件中。
            c：同时要在各个的case yml文件中留module_flag,其值为 不同模块的简写，这样方便后期处理
            d：各个host的优先级为：jenkins > config.yml > caseyml 
        
        还有另一种解决方案：
        如果各个模块之前没有关联，或者没有业务上的耦合，或者不进行业务上的交集操作，则可以进行如下操作
        1：yml文件中 不在写 module_flag，仍然留现在的写法，只有host
        2：在config.yml 和 jenkins上 配置host
        3：各个模块的代码(主要是case 和 config.yml) 提交到不同的分支中。
        host的优先级：
        jenkins > config.yml > caseyml
        
        于20220704早会沟通得知：
        1：接口最后还会投入到灰度与生产环境的验证
        2：还是要适配各个功能模块的域名。留出相应的扩展
        '''
        if "$" in procotol or "$" in host:
            url = f"{procotol}://{host}/{path}"
        else:
            url = parse.urljoin(f"{procotol}://{host}", path)

        depend_list = casedata['depends_on']

        data_str = simplejson.dumps(casedata, indent=4, ensure_ascii=False, encoding='utf-8')

        data_tmp = Template(data_str).safe_substitute(url=url)
        # 再将str格式的dict数据转化为 dict对象
        casedata = simplejson.loads(data_tmp, encoding='utf8')

        # 下面进行数据返回***************************
        request_list: list = casedata['request_params']
        desc_list: list = casedata['description']
        assert_list: list = casedata['assert']
        response_list: list = casedata['response']
        params_list = []
        requ_count = len(request_list)
        resp_count = 0
        # 判断是否需要处理响应结果。只有当为list时，且长度大于1时，才表示要处理相应的响应结果
        if isinstance(response_list, list) and len(response_list) > 0:
            resp_count = len(response_list)
        # 判断是否是否有数据依赖，逻辑同上
        depend_count = 0
        if isinstance(depend_list, list) and len(depend_list) > 0:
            depend_count = len(depend_list)

        for i in range(requ_count):
            if i <= (resp_count - 1) and i <= (depend_count - 1):
                tmp = [request_list[i], desc_list[i], assert_list[i], response_list[i], depend_list[i],run,story]
            elif i <= resp_count - 1:
                tmp = [request_list[i], desc_list[i], assert_list[i], response_list[i], None,run,story]
            elif i <= depend_count - 1:
                tmp = [request_list[i], desc_list[i], assert_list[i], None, depend_list[i],run,story]
            else:
                tmp = [request_list[i], desc_list[i], assert_list[i], None, None,run,story]

            params_list.append(tmp)

        return params_list

def get_params(ymldata: dict, caseymlname: str) -> list:
    '''
    需要传入yml文件的数据、case对应的yml文件中的key \n
    返回[[请求参数,case描述,断言,响应结果的处理,依赖的数据,是否运行,story模块],[……]……]
    :param ymldata:  yml文件的数据。
    :param caseymlname: case对应的yml文件中的key，如login
    :return: list[[req,desc,asert,resp,depend,run,story],[req,desc,asert,resp,depend,run,story],……]
    '''

    if isinstance(ymldata, dict) and len(ymldata) > 1:
        pass
    else:
        pytest.fail(f"传入的的yml数据错误，内容为：{ymldata}")

    if isinstance(caseymlname, str) and caseymlname.strip() != "":
        caseymlname = caseymlname.strip()
    else:
        pytest.fail(f"传入的case对应的yml文件中的key的名字错误,值为：{caseymlname}")

    # 获取case对应的yaml数据
    casedata: dict = ymldata.get(caseymlname)
    path = casedata['path']
    # 全局procotol
    g_procotol = ymldata.get('procotol')
    # 全局host
    g_host = ymldata.get('host')
    # case 自己的host与procotol
    m_host = casedata.get('host')
    m_procotol = casedata.get('procotol')
    run = True
    story = casedata.get('story')
    if casedata.get('run') == False:
        run = False

    # print(f"{'*'*20}run : {run}")
    # print(f"{'*'*20}story : {story}")

    # 判断模块自己的host与procotol
    # 当模块自己的host为空或None时，使用全局的。暂不考虑使用全局进行替换
    host = m_host
    procotol = m_procotol
    if m_host == None or m_host == "":
        # 判断全局的host是否也为空
        if g_host == None or g_host == "":
            host = "$host"
        else:
            host = g_host

    if m_procotol == None or m_procotol == "":
        if g_procotol == None or g_procotol == "":
            procotol = "$procotol"
        else:
            procotol = g_procotol

    # if host == None or host == "":
    #     host = "$host"
    #
    # if procotol == None or procotol == "":
    #     procotol = "$procotol"
    
    # 这里使用模板技术，方便从config.yml 文件中读取host和procotol进行替换。
    '''
    1：这里需要注意及确认的是：是每个模块的host 都是一样的，还是说不同的模块的host都不一样？需要找恩强确认
    2：从jenkins中获取到的host是在此时进行替换，还是在哪里进行替换
    3：从config.yml 中获取到的host该当怎样处理
    4：当不同模块的host 不一样时，方案如下：
        a：将所有的模块全部收集起来，目前有3个，不同模块的host 可以简写，如：V5的登录相关：v5_host,v6_host
        b：将这些host全部写在每个yaml和config.yml文件中。
        c：同时要在各个的case yml文件中留module_flag,其值为 不同模块的简写，这样方便后期处理
        d：各个host的优先级为：jenkins > config.yml > caseyml 

    还有另一种解决方案：
    如果各个模块之前没有关联，或者没有业务上的耦合，或者不进行业务上的交集操作，则可以进行如下操作
    1：yml文件中 不在写 module_flag，仍然留现在的写法，只有host
    2：在config.yml 和 jenkins上 配置host
    3：各个模块的代码(主要是case 和 config.yml) 提交到不同的分支中。
    host的优先级：
    jenkins > config.yml > caseyml

    于20220704早会沟通得知：
    1：接口最后还会投入到灰度与生产环境的验证
    2：还是要适配各个功能模块的域名。留出相应的扩展
    '''
    if "$" in procotol or "$" in host:
        url = f"{procotol}://{host}/{path}"
    else:
        url = parse.urljoin(f"{procotol}://{host}", path)

    depend_list = casedata['depends_on']

    data_str = simplejson.dumps(casedata, indent=4, ensure_ascii=False, encoding='utf-8')

    data_tmp = Template(data_str).safe_substitute(url=url)
    # 再将str格式的dict数据转化为 dict对象
    casedata = simplejson.loads(data_tmp, encoding='utf8')

    # 下面进行数据返回***************************
    request_list: list = casedata['request_params']
    desc_list: list = casedata['description']
    assert_list: list = casedata['assert']
    response_list: list = casedata['response']
    params_list = []
    requ_count = len(request_list)
    resp_count = 0
    # 判断是否需要处理响应结果。只有当为list时，且长度大于1时，才表示要处理相应的响应结果
    if isinstance(response_list, list) and len(response_list) > 0:
        resp_count = len(response_list)
    # 判断是否是否有数据依赖，逻辑同上
    depend_count = 0
    if isinstance(depend_list, list) and len(depend_list) > 0:
        depend_count = len(depend_list)

    for i in range(requ_count):
        if i <= (resp_count - 1) and i <= (depend_count - 1):
            tmp = [request_list[i], desc_list[i], assert_list[i], response_list[i], depend_list[i], run, story]
        elif i <= resp_count - 1:
            tmp = [request_list[i], desc_list[i], assert_list[i], response_list[i], None, run, story]
        elif i <= depend_count - 1:
            tmp = [request_list[i], desc_list[i], assert_list[i], None, depend_list[i], run, story]
        else:
            tmp = [request_list[i], desc_list[i], assert_list[i], None, None, run, story]

        params_list.append(tmp)

    return params_list

