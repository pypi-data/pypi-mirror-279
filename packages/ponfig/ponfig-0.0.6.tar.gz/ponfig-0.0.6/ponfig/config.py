import os

def find_config_file(filename, start_path):
    current_path = start_path
    while current_path != os.path.dirname(current_path):
        potential_path = os.path.join(current_path, 'config', filename)
        if os.path.exists(potential_path):
            return potential_path
        current_path = os.path.dirname(current_path)
    raise FileNotFoundError(f"{filename} not found in any config directory.")

def get_config(key):
    start_path = os.path.abspath(os.path.dirname(__file__))
    config_path = find_config_file('app.config', start_path)
    
    with open(config_path, 'r') as file:
        for line in file:
            if line.strip() and not line.startswith('#'):
                k, v = line.split('=', 1)
                if k.strip() == key:
                    return v.strip()
    raise KeyError(f"{key} not found in {config_path}.")
