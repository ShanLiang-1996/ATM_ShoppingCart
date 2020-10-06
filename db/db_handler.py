"""
用于处理数据
"""
import os
import json
from conf import settings


def select(usrname):
    file_path = os.path.join(settings.USER_DATA_DIR, usrname + '.json')
    if os.path.exists(file_path):
        with open(file_path, 'r') as fp:
            usr_data = json.load(fp)
        return usr_data


def create(usr_data):

    usrname = usr_data['usrname']
    file_path = os.path.join(settings.USER_DATA_DIR, usrname + '.json')

    with open(file_path, 'w') as fp:
        usr_data_json = json.dumps(usr_data, indent=4)
        fp.write(usr_data_json)
