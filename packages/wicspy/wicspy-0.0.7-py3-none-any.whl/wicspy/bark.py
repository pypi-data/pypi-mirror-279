'''
Author: wicsp wicspa@gmail.com
Date: 2024-06-05 14:53:56
LastEditors: wicsp wicspa@gmail.com
LastEditTime: 2024-06-05 16:10:06
FilePath: /wicspy/bark.py
Description: 

Copyright (c) 2024 by wicsp, All Rights Reserved. 
'''
import os
import requests
from loguru import logger

# 读取环境变量
BARK_ID = os.environ.get('BARK_ID')

if not BARK_ID:
    raise ValueError("BARK_ID is not set in environment variables, Please add `export BARK_ID=your_bark_id` to your shell profile file, and then run `source ~/.bashrc` or `source ~/.zshrc` to take effect.")

def bark(title:str, content:str, group:str = None, bark_id=BARK_ID) -> None:
    """send message via bark

    Args:
        title (str): _description_
        content (str): _description_
        group (str, optional): _description_. Defaults to None.
        bark_id (_type_, optional): _description_. Defaults to BARK_ID.
    """
    logger.add("log/bark.log", rotation="100KB", retention="10 days")

    reminder_url = f"https://api.day.app/{bark_id}/{title}/{content}"
    params = {}
    if group:
        params['group'] = group
    try:
        response = requests.post(reminder_url, params=params)
        response.raise_for_status()  # 检查请求是否成功
        logger.info(f"提醒发送成功: {title} >{content}")
    except requests.exceptions.RequestException as e:
        logger.error(f"提醒发送成功: {title} >{content}")


