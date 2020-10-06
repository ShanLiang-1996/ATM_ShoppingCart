"""
存放公共方法
"""
import time
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
