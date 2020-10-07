"""
存放公共方法
"""
import time
import hashlib
import core
from db import db_handler


def exit_in_t(t, str="将在%ss后返回"):
    if '%s' not in str:
        str += '%s'
    while t > 0:
        print(str % t,end="")
        time.sleep(1)
        print("\r",end="",flush = True)
        t -= 1


def disp_basic_info(usr_data):
    disp_str = \
        f"""
    Hi, {usr_data['usrname']}:
    账户额度：{usr_data['credit_limit']}
    剩余额度：{usr_data['balance']}
    购物车：{usr_data['shopping_cart']}
        """
    return disp_str


def get_pwd_md5(password):
    md5_obj = hashlib.md5()
    md5_obj.update(password.encode('utf-8'))
    salt = "The World You Love."
    md5_obj.update(salt.encode('utf-8'))

    return md5_obj.hexdigest()

def check_login(func):
    def swapper(*args, **kwargs):
        from core.src import g_current_account
        if g_current_account:
            res = func(*args, **kwargs)
            return res
        else:
            print("当前用户未登陆，请重新登录。")
            core.src.login()

    return swapper
