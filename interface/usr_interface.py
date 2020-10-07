"""
用户相关业务借口
"""
from db import db_handler
from lib import common

def regist(usrname, password, limit=15000):

    if db_handler.select(usrname):
        return False, "当前用户名已存在，请重新输入！"
    else:
        password = common.get_pwd_md5(password)
        usr_profile = {
            'usrname': usrname,
            'password': password,
            'credit_limit': limit,
            'balance': limit,
            'shopping_cart': {},
            'statement': {},
            'isfreeze': False,
        }

        try:
            db_handler.create(usr_profile)
        except e:
            print(e)
            return False, "创建用户过程中出现错误，请稍后再试！"
        else:
            return True, "用户创建成功！"


def login(usrname, password):

    if usr_data := db_handler.select(usrname):

        password = common.get_pwd_md5(password)
        if usr_data['password'] == password:
            return 'sucess', common.disp_basic_info(usr_data)
        else:
            return 'pwd_err', '密码输入错误！'

    else:
        return 'usr_non-existent', '用户名不存在！'


def check_balance(usrname):

    usr_data = db_handler.select(usrname)
    return common.disp_basic_info(usr_data)
