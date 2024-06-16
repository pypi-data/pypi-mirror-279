import os

def find_env_file(filename, start_path):
    current_path = start_path
    while current_path != os.path.dirname(current_path):
        potential_path = os.path.join(current_path, 'env', filename)
        if os.path.exists(potential_path):
            return potential_path
        current_path = os.path.dirname(current_path)
    raise FileNotFoundError(f"{filename} not found in any env directory.")

def get_env(key):
    start_path = os.path.abspath(os.path.dirname(__file__))
    env_path = find_env_file('app.env', start_path)
    
    with open(env_path, 'r') as file:
        for line in file:
            if line.strip() and not line.startswith('#'):
                k, v = line.split('=', 1)
                if k.strip() == key:
                    return v.strip()
    raise KeyError(f"{key} not found in {env_path}.")
