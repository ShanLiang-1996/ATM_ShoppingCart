"""
银行相关业务借口
"""
from db import db_handler

def usr_authenticate(func):
    def swapper(*args, **kwargs):
        print(f"当前用户：{kwargs['account']}")
        current_account_data = db_handler.select(kwargs['account'])
        err_times = 0
        while err_times < 3:
            input_password = input("请输入您的密码以确认您的操作：")
            if current_account_data['password'] == input_password:
                print("认证成功！")
                res = func(*args, **kwargs)
                break
            else:
                print("输入错误！")
                err_times += 1
        return res
    return swapper


@usr_authenticate
def withdraw(account, amount):
    current_account_data = db_handler.select(account)
    deduction = round(1.05 * float(amount), 2)

    if deduction <= current_account_data['balance']:
        current_account_data['balance'] -= deduction
        db_handler.create(current_account_data)
        return True, f"提现{amount}元，剩余额度{current_account_data['balance']}。"
    else:
        return False, "余额不足！"


@usr_authenticate
def repay(account, amount):
    data = db_handler.select(account)
    if data['balance'] == data['credit_limit']:
        return False, "您当前无需还款。"
    if (new_balance := float(amount) + data['balance']) <= data['credit_limit']:
        data['balance'] = new_balance
        db_handler.create(data)
        return True, f"还款成功，剩余额度{data['balance']}。"
    else:
        return_amount = round(new_balance - data['credit_limit'], 2) 
        data['balance'] = data['credit_limit']
        db_handler.create(data)
        return False, f"您的还款额太多了，已为您恢复最大额度。退还：{return_amount}"
