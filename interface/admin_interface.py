import os

from db import db_handler
from conf import settings

def check_usrs():
    usr_files = os.listdir(settings.USER_DATA_DIR)
    res = []
    for usr_file in usr_files:
        res.append(usr_file[:-5])
    return res

def change_limit(usr, limit):
    limit = round(float(limit), 2)
    if data := db_handler.select(usr):
        delta = limit - data['credit_limit']
        data['credit_limit'] = limit
        data['balance'] += delta
        db_handler.create(data)
        return True, f"用户{usr}额度修改成功，当前额度为{limit}"
    else:
        return False, f"用户{usr}不存在！"

def freeeze_usr(usr):

    if data := db_handler.select(usr):
        data['isfreeze'] = True
        db_handler.create(data)
        return True, f"用户{usr}已冻结！"
    else:
        return False, f"用户{usr}不存在！"
