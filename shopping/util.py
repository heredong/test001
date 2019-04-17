import datetime
import random
import uuid
import hashlib

def get_unique_name():
    uuid_str = str(uuid.uuid4()).encode('utf-8')

    md5 = hashlib.md5()

    md5.update(uuid_str)

    return md5.hexdigest().lower()

def get_sum_money(cartitems):
    sum_money = 0
    for i in cartitems.filter(is_select=True):
        sum_money += (i.num * i.goods.price)
    return sum_money

def get_order_number():
    uuid_str = uuid.uuid4().hex
    now_str = datetime.datetime.now().strftime("%Y%m%d%H%M")

    number = now_str + uuid_str[:20]
    return number