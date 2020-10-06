"""
银行相关业务借口
"""

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
