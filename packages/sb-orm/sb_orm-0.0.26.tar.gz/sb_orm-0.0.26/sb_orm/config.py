import os
from os import getenv
from dotenv import load_dotenv

BASE_DIR = os.getcwd()
load_dotenv(os.path.join(BASE_DIR, '.env'))


# 获取环境变量
def env(key, default_value: str = None):
    val = getenv(key)
    if val is None:
        if default_value is not None:
            return default_value
        else:
            print(f"{key}环境变量为空")
    return val
