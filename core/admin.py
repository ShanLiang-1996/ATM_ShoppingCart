from interface import admin_interface
from core import src
# 1. 查看所有用户
def check_usrs():
    msg = admin_interface.check_usrs()
    print(msg)


# 2. 添加用户
def add_usr():
    src.register()


# 3. 变更用户额度
def change_limit():
    usr = input("请输入需要修改的用户名：")
    limit = input(f"请输入{usr}的新额度：")

    state, msg = admin_interface.change_limit(usr, limit)
    print(msg)


# 4. 冻结用户
def freeeze_usr():
    usr = input("请输入需要冻结的账户：")
    state, msg = admin_interface.freeeze_usr(usr)
    print(msg)


# 5. 登出
def logout():
    src.run()




def run():
    admin_func = {
        '1': check_usrs,
        '2': add_usr,
        '3': change_limit,
        '4': freeeze_usr,
        '5': logout,
    }

    while True:
        print("""
============ admin ============
    1. 查看所有用户
    2. 添加用户
    3. 变更用户额度
    4. 冻结用户
    5. 登出
============= end =============
        """)

        choice = input("请输入管理员功能：").strip()
        admin_func[choice]()
