import os


class UserConfig:
    default_group_name = "默认分组"


class FileConfig:
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static/files')
    FILE_URL = 'static/files'


def get_boolean(p):
    return p in ['true', 'True', 'TRUE', 't', 'T']
