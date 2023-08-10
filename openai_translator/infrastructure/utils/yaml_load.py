import yaml

def load(file_path):
    with open(file_path, "r") as f:
         result = yaml.safe_load(f)
    return result