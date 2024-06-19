'''
Author: wicsp wicspa@gmail.com
Date: 2024-06-18 19:12:15
LastEditors: wicsp wicspa@gmail.com
LastEditTime: 2024-06-18 19:18:19
FilePath: /wicspy/wicspy/timer_tool.py
Description: 

Copyright (c) 2024 by wicsp, All Rights Reserved. 
'''
import time
import functools


def timing(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()  # 记录开始时间
        result = func(*args, **kwargs)  # 执行函数
        end_time = time.time()  # 记录结束时间
        elapsed_time = end_time - start_time  # 计算经过的时间
        print(
            f"Function '{func.__name__}' executed in {elapsed_time:.4f} seconds")
        return result
    return wrapper
