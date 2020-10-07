"""
用于存放用户视图层
"""
import time
from interface import usr_interface, bank_interface,shop_interface
from lib.common import exit_in_t, check_login
from core import admin

global g_current_account
g_current_account = None

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
                global g_current_account
                g_current_account = usrname
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
            global g_current_account
            g_current_account = usrname
            exit_in_t(1, "将会在%ss后返回主界面")
            break

# 3. 查看余额
@check_login
def check_balance():
    global g_current_account
    print(usr_interface.check_balance(g_current_account))
    exit_in_t(3, "将会在%ss后返回主界面")

# 4. 提现
@check_login
def withdraw():
    global g_current_account

    amount = input("请输入您想要提现的金额：")
    state, msg = bank_interface.withdraw(account=g_current_account,
                                         amount=amount)
    print(msg)


# 5. 还款
@check_login
def repay():
    global g_current_account
    amount = input("请输入您想要还款的金额：")
    state, msg = bank_interface.repay(account=g_current_account,
                                      amount=amount)
    print(msg)


# 6. 转账
@check_login
def transfer():
    global g_current_account
    target_account = input("请输入转账账户：")
    amount = input("请输入转账金额：")
    state, msg = bank_interface.transfer(account=g_current_account,
                                         target_account=target_account,
                                         amount=amount)
    print(msg)

# 7. 查看流水
@check_login
def check_statement():
    global g_current_account
    state, msg = bank_interface.check_statement(account=g_current_account)
    print(msg)

# 8. 购物
@check_login
def shopping():

    good_list = [
        ['上海灌汤包', 30],
        ['特斯拉', 150000],
        ['泡椒凤爪', 15],
        ['香港地道鱼丸', 20],
        ['macbook pro', 17000],
        ['macbook air', 12000],
    ]

    shopping_cart = {}

    while True:

        for index, good in enumerate(good_list):
            good_name, good_price = good
            print(f'商品编号为{index}',
                  f'商品名称：{good_name}',
                  f'商品单价：{good_price}')

        choice = input('请输入商品编号(若结账当前购物车请输入y，储存当前购物车请输入n)：').strip()

        if choice == 'y':
            if not shopping_cart:
                print("当前购物车为空，请添加商品！")
                continue

            state, msg = shop_interface.shopping(g_current_account,
                                                 shopping_cart)
            print(msg)
            if state: break
            else: continue

        elif choice == 'n':
            if not shopping_cart:
                print("当前购物车为空，请添加商品！")
                continue

            state, msg = shop_interface.add_to_cart(g_current_account,
                                                    shopping_cart)
            print(msg)
            if state: break
            else: continue


        if not choice.isdigit():
            print("请输入正确的商品编号！")
            continue
        choice = int(choice)

        if choice not in range(len(good_list)):
            print("请输入正确的商品编号！")
            continue

        good_name, good_price = good_list[choice]

        if good_name in shopping_cart.keys():
            shopping_cart[good_name][1] += 1
        else:
            shopping_cart[good_name] = [good_price, 1]



# 9. 查看购物车
@check_login
def check_shopping_cart():
    msg = shop_interface.check_shopping_cart(g_current_account)
    print(msg)

    while True:
        choice = input("现在购买请输入1，稍后购买请输入2：").strip()
        if choice == '1':
            _, shopping_msg = shop_interface.shopping(g_current_account, msg)
            print(shopping_msg)
            break
        elif choice == '2':
            break
        else:
            print("输入错误请重新输入")
# 10. 管理员
def admin_func():
    admin.run()

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
    '0': admin_func,
    'q': exit_program,
}


def run():

    global g_current_account

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
