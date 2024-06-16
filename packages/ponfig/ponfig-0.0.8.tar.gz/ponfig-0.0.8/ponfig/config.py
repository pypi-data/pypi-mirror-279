# ponfig/config.py

import os

def get_project_root():
    return os.path.abspath(os.getcwd())

def get_config(key):
    config_path = os.path.join(get_project_root(), 'config', 'app.config')
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"{config_path} does not exist.")
    
    with open(config_path, 'r') as file:
        for line in file:
            if line.strip() and not line.startswith('#'):
                k, v = line.split('=', 1)
                if k.strip() == key:
                    return v.strip()
    raise KeyError(f"{key} not found in {config_path}.")

# 创建或更新配置文件
def set_config(key, value):
    config_path = os.path.join(get_project_root(), 'config', 'app.config')
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"{config_path} does not exist.")
    
    with open(config_path, 'r') as file:
        lines = file.readlines()
    
    with open(config_path, 'w') as file:
        for line in lines:
            if line.strip() and not line.startswith('#'):
                k, v = line.split('=', 1)
                if k.strip() == key:
                    line = f"{key}={value}\n"
            file.write(line)

