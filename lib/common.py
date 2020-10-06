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
    剩余额度：{usr_data['credit_limit'] - usr_data['balance']}
    购物车：{usr_data['balance']}
        """
    return disp_str


def usr_authenticate(current_account):
    print(current_account)
    def my_dacerator(func):
        def swapper(*args, **kwargs):
            print(current_account)
            current_account_data = db_handler.select(current_account)
            err_times = 0
            while err_times < 3:
                input_password = input("请输入您的密码以确认您的操作：")
                if current_account_data['password'] == password:
                    print("认证成功！")
                    func(*args, **kwargs)
                    break
                else:
                    print("输入错误！")
                    err_times += 1
        return swapper
    return my_dacerator
