import os

home_config_path = os.path.join(os.path.expanduser("~"), ".zus")

def get_app_config_path(app: str):
    assert os.sep not in app, "app name cannot contain a path separator"
    path = os.path.join(home_config_path, app)
    os.makedirs(path, exist_ok=True)
    return path
