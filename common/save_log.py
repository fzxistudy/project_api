# -*- coding: UTF-8 -*- 
# 设置utf-8  显示中文
"""
@Create Time: 2022-7-11 19:58
@Author: test
@File：save_log.py
"""
import os
import logging
from common.get_config_data import GetConfData
from common.get_datetime import GetDateTime


confdata = GetConfData.get_instance()
dt = GetDateTime()
curdate = dt.get_curdate()
runlog_dir = confdata.get_runlog_dir_path()
# 设置log日志文件名称
log_name = f"api_run_{curdate}.log"
# 拼接日志路径
log_path = os.path.join(runlog_dir,log_name)

# 实例化loggerr对象
logger = logging.getLogger(__name__)

# 绑定log的handler
file_handler = logging.FileHandler(filename=log_path,encoding='utf-8')

# 输出formatter
# fmt = '[%(asctime).19s] %(process)d:%(levelname).1s %(filename)s:%(lineno)d:%(funcName)s: %(message)s]'
fmt = f'[%(asctime).19s] %(process)d:%(levelname).1s %(message)s]'
formatter = logging.Formatter(fmt)

# 日志格式与句柄的绑定
file_handler.setFormatter(formatter)
# 控制台句柄定义
steam_handler = logging.StreamHandler()
# 日志格式与句柄的绑定
steam_handler.setFormatter(formatter)
# 与logger进行绑定
logger.addHandler(file_handler)
logger.addHandler(steam_handler)
# 设置展示/写入文件的日志的级别
logger.setLevel(logging.INFO)
