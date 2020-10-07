"""
银行相关业务借口
"""
from db import db_handler
from lib import common
import datetime

def usr_authenticate(func):
    def swapper(*args, **kwargs):
        print(f"当前用户：{kwargs['account']}")
        current_account_data = db_handler.select(kwargs['account'])
        err_times = 0
        while err_times < 3:
            input_password = input("请输入您的密码以确认您的操作：")
            input_password = common.get_pwd_md5(input_password)
            if current_account_data['password'] == input_password:
                print("认证成功！")
                res = func(*args, **kwargs)
                return res
            else:
                print("输入错误！")
                err_times += 1
        return False, "连续三次输入密码错误！"
    return swapper

def get_operation(operation_type, amount):
    now = datetime.datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S")
    return {now: (operation_type, amount)}


@usr_authenticate
def withdraw(account, amount):
    current_account_data = db_handler.select(account)
    deduction = round(1.05 * float(amount), 2)

    if deduction <= current_account_data['balance']:
        current_account_data['balance'] -= deduction

        operation = get_operation('withdraw', -1 * deduction)
        current_account_data['statement'].update(operation)

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

        operation = get_operation('repay', amount)
        data['statement'].update(operation)
        db_handler.create(data)

        return True, f"还款成功，剩余额度{data['balance']}。"
    else:

        return_amount = round(new_balance - data['credit_limit'], 2)

        operation = get_operation('repay', amount - return_amount)
        data.update(operation)
        data['balance'] = data['credit_limit']
        db_handler.create(data)

        return True, f"您的还款额太多了，已为您恢复最大额度。退还：{return_amount}"


@usr_authenticate
def transfer(account, target_account, amount):

    data = db_handler.select(account)

    amount = round(float(amount), 2)
    if target_data := db_handler.select(target_account):

        if amount <= data['balance']:

            operation = get_operation('transfer', -1 * amount)
            data['statement'].update(operation)
            operation = get_operation('receive', amount)
            target_data['statement'].update(operation)

            data['balance'] -= amount
            target_data['balance'] += amount
            db_handler.create(data)
            db_handler.create(target_data)
            return True, f"转账成功，当前账户余额{data['balance']}"
        else:
            return False, "当前账户余额不足！"

    else:
        return False, "目标账户不存在！"

@usr_authenticate
def pay(account, cost):

    data = db_handler.select(account)

    if data['balance'] < cost:
        return False
    else:
        data['balance'] -= cost
        operation = get_operation('payment', -1 * cost)
        data['statement'].update(operation)
        db_handler.create(data)
        return True


@usr_authenticate
def check_statement(account):
    data = db_handler.select(account)
    return True, data['statement']
