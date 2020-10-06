"""
用于存放用户视图层
"""
import time
from interface import usr_interface
from lib import common

# 1. 注册
def register():

    while True:
        usrname = input("请输入用户名：")
        password = input("请输入密码：")
        confirm_password = input("请再次输入密码：")

        if password == confirm_password:
            # call regist func
            state, msg = usr_interface.regist(usrname, password)
            print(msg)

            if state:
                break
        else:
            print("两次输入密码不匹配，请重新输入密码！")

# 2. 登录
def login():

    pwd_err_count = 0

    while pwd_err_count < 3:

        usrname = input("请输入用户名：")
        password = input("请输入密码：")
        state, msg = usr_interface.login(usrname, password)

        print(msg)
        if state == "pwd_err":
            pwd_err_count += 1
            print(f"输入错误{pwd_err_count}次，账户将会在{3 - pwd_err_count}次后冻结。")
        elif state == "usr_non-existent":
            continue
        elif state == "sucess":
            global current_account
            current_account = usrname
            common.exit_in_t(10, "将会在%ss后返回主界面")
            break

# 3. 查看余额
def check_balance():
    global current_account
    if not current_account:
        print("当前用户未登陆！请重新登陆。")
    else:
        print(usr_interface.check_balance(current_account))
        common.exit_in_t(10, "将会在%ss后返回主界面")

# 4. 提现
def withdraw():

    pass
# 5. 还款
def repay():

    pass
# 6. 转账
def transfer():

    pass
# 7. 查看流水
def check_statement():

    pass
# 8. 购物
def shopping():

    pass
# 9. 查看购物车
def check_shopping_cart():

    pass
# 10. 管理员
def admin():

    pass

def exit_program():
    exit(0)

func_dict = {
    '1': register,
    '2': login,
    '3': check_balance,
    '4': withdraw,
    '5': repay,
    '6': transfer,
    '7': check_statement,
    '8': shopping,
    '9': check_shopping_cart,
    '0': admin,
    'q': exit_program,
}



def run():
    current_account = None
    while True:
        print("""
===== ATM + ShoppingCart =====
    1. 注册
    2. 登录
    3. 查看余额
    4. 提现
    5. 还款
    6. 转账
    7. 查看流水
    8. 购物
    9. 查看购物车
    0. 管理员
    q. 退出程序
============= end =============
        """)

        choice = input("请选择你需要的功能: ").strip()

        if choice not in func_dict.keys():
            print("你输入的功能不存在，请重新输入！")
            continue
        else:
            func_dict[choice]()
