"""
购物相关接口
"""
from interface import bank_interface
from db import db_handler
from lib import common

usr_logger = common.get_logger('user')

def shopping(usr, shopping_cart):

    cost = 0
    for good_price, good_num in shopping_cart.values():
        cost += good_price * good_num

    state = bank_interface.pay(account=usr, cost=cost)

    if state:
        return True, f"支付{cost}元，准备发货！"
    else:
        return False, "支付失败，账户余额不足。"


def check_shopping_cart(usr):
    data = db_handler.select(usr)
    return data['shopping_cart']

def add_to_cart(usr, shopping_cart):

    data = db_handler.select(usr)
    origin_cart = data['shopping_cart']

    for good in shopping_cart.keys():

        if good in origin_cart.keys():
            data['shopping_cart'][good][1] += shopping_cart[good][1]
        else:
            data['shopping_cart'].update({good: shopping_cart[good]})

    try:
        db_handler.create(data)
    except e:
        return False, "购物车储存失败，请稍后重试..."
    else:
        return True, "购物车保存成功，欢迎下次光临。"
