# ponfig/env.py

import os

def get_project_root():
    return os.path.abspath(os.getcwd())

def get_env(key):
    env_path = os.path.join(get_project_root(), 'env', 'app.env')
    if not os.path.exists(env_path):
        raise FileNotFoundError(f"{env_path} does not exist.")
    
    with open(env_path, 'r') as file:
        for line in file:
            if line.strip() and not line.startswith('#'):
                k, v = line.split('=', 1)
                if k.strip() == key:
                    return v.strip()
    raise KeyError(f"{key} not found in {env_path}.")

# 创建或更新环境变量
def set_env(key, value):
    env_path = os.path.join(get_project_root(), 'env', 'app.env')
    if not os.path.exists(env_path):
        raise FileNotFoundError(f"{env_path} does not exist.")
    
    with open(env_path, 'r') as file:
        lines = file.readlines()
    
    with open(env_path, 'w') as file:
        for line in lines:
            if line.strip() and not line.startswith('#'):
                k, v = line.split('=', 1)
                if k.strip() == key:
                    line = f"{key}={value}\n"
            file.write(line)