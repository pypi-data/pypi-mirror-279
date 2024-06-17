import json

from .. import app_settings


def show_status() -> None:
    print("Settings:")
    print(json.dumps(app_settings.__dict__, indent=4))
