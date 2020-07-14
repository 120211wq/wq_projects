import datetime
import json
import random
import time

import requests
from dateutil.relativedelta import relativedelta

from xlog import XLog
from addr import addr

null = None
true = True
false = False

header = {"Content-Type": "application/json", "Access-Token": ""}


def get_random_name():
    a1 = ['张', '刘', '李', '王', '赵', '林']
    a2 = ['玉', '明', '龙', '芳', '军', '玲', '舒', '丽', '伟', '忠', '达']
    a3 = ['', '立', '玲', '', '国', '强', '杰', '轩', '', '']
    for i in range(15):
        name = random.choice(a1) + random.choice(a2) + random.choice(a3)
        return name


def getCheckBit(num17):
    """
    获取身份证最后一位，即校验码
    :param num17: 身份证前17位字符串
    :return: 身份证最后一位
    """
    Wi = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    checkCode = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
    zipWiNum17 = zip(list(num17), Wi)
    S = sum(int(i) * j for i, j in zipWiNum17)
    Y = S % 11
    return checkCode[Y]


def getAddrCode():
    """
    获取身份证前6位，即地址码
    :return: 身份证前6位
    """
    addrIndex = random.randint(0, len(addr) - 1)
    return addr[addrIndex]


def getBirthday(start="1900-01-01", end="2017-12-30"):
    """
    获取身份证7到14位，即出生年月日
    :param start: 出生日期合理的起始时间
    :param end: 出生日期合理的结束时间
    :return: 份证7到14位
    """
    days = (datetime.datetime.strptime(end, "%Y-%m-%d") - datetime.datetime.strptime(start, "%Y-%m-%d")).days + 1
    birthday = datetime.datetime.strptime(start, "%Y-%m-%d") + datetime.timedelta(random.randint(0, days))
    return datetime.datetime.strftime(birthday, "%Y%m%d")


def getRandomIdCard(sex=1):
    """
    获取随机身份证
    :param sex: 性别，默认为男
    :return: 返回一个随机身份证
    """
    idNumber, addrName = getAddrCode()
    idCode = str(idNumber) + getBirthday()
    for i in range(2):
        idCode += str(random.randint(0, 9))
    idCode += str(random.randrange(sex, 9, 2))
    idCode += getCheckBit(idCode)
    return idCode


def RandomPhone():
    prelist = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "147", "150", "151", "152",
               "153", "155", "156", "157", "158", "159", "186", "187", "188"]
    randomPre = random.choice(prelist)
    Number = "".join(random.choice("0123456789") for i in range(8))
    phoneNum = randomPre + Number
    return phoneNum


def time2seconds(t):
    h, m, s = t.strip().split(":")
    return int(h) * 3600 + int(m) * 60 + int(s)


def seconds2time(sec):
    m, s = divmod(sec, 60)
    h, m = divmod(m, 60)
    return "%02d:%02d:%02d" % (h, m, s)


def random_car_type():
    lists = ['宝马', '大众', '日产', '吉利', '长城', '马自达', '沃尔沃', '奔驰', '本田', '丰田', '雪佛兰']
    return random.choice(lists)


def random_car():
    return '粤A' + "".join(
        random.sample(['A', 'B', 'C', 'D', 'E', 'F', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], 5)).replace(" ",
                                                                                                                    "")


def random_creat_date():
    st = "11:00:00"
    et = "13:00:00"
    # st = "08:16:00"
    # et = "08:17:00"
    day = datetime.datetime.now().strftime('%Y-%m-%d')
    sts = time2seconds(st)
    ets = time2seconds(et)
    rt = random.sample(range(sts, ets), 1)
    times = seconds2time(rt[0])
    return day + 'T' + str(times) + '.000Z'


def random_approve_date():
    st = "00:00:00"
    et = "03:00:00"
    # st = "07:50:00"
    # et = "07:55:00"
    day = datetime.date.today().strftime('%Y-%m-%d')
    sts = time2seconds(st)
    ets = time2seconds(et)
    rt = random.sample(range(sts, ets), 1)
    times = seconds2time(rt[0])
    return day + 'T' + str(times) + '.000Z'


def random_visitor_arrive_date():
    st = "02:00:00"
    et = "05:00:00"
    # st = "08:00:00"
    # et = "08:05:00"
    day = datetime.date.today().strftime('%Y-%m-%d')
    sts = time2seconds(st)
    ets = time2seconds(et)
    rt = random.sample(range(sts, ets), 1)
    times = seconds2time(rt[0])
    return day + 'T' + str(times) + '.000Z'


def random_owner_arrive_date():
    st = "00:00:00"
    et = "12:00:00"
    # st = "08:00:00"
    # et = "08:05:00"
    day = datetime.date.today().strftime('%Y-%m-%d')
    sts = time2seconds(st)
    ets = time2seconds(et)
    rt = random.sample(range(sts, ets), 1)
    times = seconds2time(rt[0])
    return day + 'T' + str(times) + '.000Z'


def login():
    url = 'https://api2.xlink.cn/v2/corp_auth'
    body = {"account": "shijie01@xlink.cn", "password": "Xlink123"}
    res = requests.post(url=url, json=body, headers=header)
    change_cont = eval(res.text)
    token1 = change_cont["access_token"]
    header['Access-Token'] = token1


def get_owner():
    url = 'https://api2.xlink.cn/v2/smart-parkinglot/xlink-carowner/owner-info?data=%7B%22offset%22:0,%22limit%22:100,%22order%22:%7B%22create_time%22:%22desc%22%7D,%22query%22:%7B%22project_id%22:%7B%22$eq%22:%222490b983d365adefc3f612d7921b6981%22%7D%7D%7D'
    body = {"offset": 0, "limit": 100, "order": {"create_time": "desc"},
            "query": {"project_id": {"$eq": "2490b983d365adefc3f612d7921b6981"}}}
    try:
        res = requests.get(url=url, json=body, headers=header)
        result = eval(res.text)
        owners = result['data']['list']
        owner = random.randint(0, len(owners) - 1)
        return owners[owner]
    except Exception:
        raise


def creat_car(own):
    url = 'https://api2.xlink.cn/v2/smart-parkinglot/xlink-carowner/owner-info/car-info'
    body = {"is_auth": true, "car_plate_no": random_car(), "carowner_name": own["owner_name"],
            "carowner_tel": own["tel"], "car_brand": random_car_type(), "license_pic_front": "", "license_pic_back": "",
            "car_pic": "", "insurance_pic_front": "", "drivers_license_pic_front": "", "drivers_license_pic_back": "",
            "project_id": "2490b983d365adefc3f612d7921b6981", "project_name": "雅湖居"}
    try:
        res = requests.post(url=url, json=body, headers=header)
        result = eval(res.text)
        return result['data']
    except Exception:
        raise


def card_apply(car, owner):
    url = 'https://api2.xlink.cn/v2/smart-parkinglot/xlink-card/apply/card-apply'
    body = {"apply_mode": 1, "car_ids": [car['id']], "car_owner_id": owner['id'],
            "card_package_id": "697888727338323968"}
    try:
        res = requests.post(url=url, json=body, headers=header)
        result = eval(res.text)
        return result['data']
    except Exception:
        raise


def get_car_place():
    url = 'https://api2.xlink.cn/v2/smart-parkinglot/xlink-park/car-place?data=%7B%22offset%22%3A0%2C%22limit%22%3A10%2C%22order%22%3A%7B%22create_date%22%3A%22desc%22%7D%2C%22query%22%3A%7B%22parkinglot_id%22%3A%7B%22%24eq%22%3A%221313348455%22%7D%2C%22parking_space_status%22%3A%7B%22%24eq%22%3A0%7D%7D%7D'
    body = {"offset": 0, "limit": 10, "order": {"create_date": "desc"},
            "query": {"parkinglot_id": {"$eq": "1313348455"}, "parking_space_status": {"$eq": 0}}}
    try:
        res = requests.get(url=url, json=body, headers=header)
        result = eval(res.text)
        return result['data']['list'][0]
    except Exception:
        raise


def get_effective_date():
    day = (datetime.date.today() + datetime.timedelta(-1)).strftime('%Y-%m-%d')
    yestoday = day + 'T16:00:00.000Z'
    url = 'https://api2.xlink.cn/v2/smart-parkinglot/xlink-card/apply/effective-date'
    body = {"card_package_id": "697888727338323968", "duration": 1, "effective_begin_date": yestoday}
    try:
        res = requests.post(url=url, json=body, headers=header)
        result = eval(res.text)
        return result['data']
    except Exception:
        raise


def card_approval(card, car_place, effective_date):
    # yestoday = (datetime.date.today() + datetime.timedelta(-1)).strftime('%Y-%m-%d')
    # begin_date = yestoday + 'T16:00:00.000Z'
    # next_month = (datetime.date.today() + datetime.timedelta(-1)) + relativedelta(months=+1)
    # end_date = str(next_month) + 'T16:00:00.000Z'
    url = 'https://api2.xlink.cn/v2/smart-parkinglot/xlink-card/apply/card-approval'
    body = {"apply_id": card, "approval_status": 1, "apply_duration": 1, "begin_date": effective_date['begin_date'],
            "end_date": effective_date['end_date'], "car_place_ids": [car_place['id']]}
    try:
        res = requests.post(url=url, json=body, headers=header)
        result = eval(res.text)
    except Exception:
        raise


def get_card_order(card):
    url = 'https://api2.xlink.cn/v2/smart-parkinglot/xlink-payment/card-order/list?data=%7B%22query%22%3A%7B%22apply_id%22%3A%7B%22%24eq%22%3A%22' + card + '%22%7D%2C%22order_type%22%3A%7B%22%24eq%22%3A0%7D%7D%7D'
    body = {"query": {"apply_id": {"$eq": card}, "order_type": {"$eq": 0}}}
    try:
        res = requests.get(url=url, json=body, headers=header)
        result = eval(res.text)
        return result['data'][0]
    except Exception:
        raise


def get_new_card_order(card):
    url = 'https://api2.xlink.cn/v2/smart-parkinglot/xlink-payment/card-order/list?data=%7B%22query%22%3A%7B%22apply_id%22%3A%7B%22%24eq%22%3A%22' + card + '%22%7D%2C%22order_type%22%3A%7B%22%24eq%22%3A1%7D%7D%7D'
    body = {"query": {"apply_id": {"$eq": card}, "order_type": {"$eq": 1}}}
    try:
        res = requests.get(url=url, json=body, headers=header)
        result = eval(res.text)
        return result['data'][0]
    except Exception:
        raise


def pay_confirm(card_order, effective_date):
    url = 'https://api2.xlink.cn/v2/smart-parkinglot/xlink-card/apply/pay-confirm'
    body = {"bill_payable": card_order['bill_payable'], "real_pay": card_order['bill_payable'], "pay_type": 10,
            "comment": "", "effective_date_begin": effective_date['begin_date'],
            "effective_date_end": effective_date['end_date'], "order_id": card_order['id']}
    try:
        res = requests.post(url=url, json=body, headers=header)
        result = eval(res.text)
    except Exception:
        raise


def get_card_apply_info(card, card_order):
    url = 'https://api2.xlink.cn/v2/smart-parkinglot/xlink-card/apply?data=%7B%22offset%22:0,%22limit%22:10,%22order%22:%7B%22create_date%22:%22desc%22%7D,%22query%22:%7B%22approval_status%22:%7B%22$ne%22:4%7D,%22apply_mode%22:%7B%22$ne%22:2%7D,%22project_id%22:%7B%22$eq%22:%22' + \
          card_order['project_id'] + '%22%7D,%0A%22id%22:%7B%22$eq%22:%22' + card + '%22%7D%7D%7D'
    body = {"offset": 0, "limit": 10, "order": {"create_date": "desc"},
            "query": {"approval_status": {"$ne": 4}, "apply_mode": {"$ne": 2},
                      "project_id": {"$eq": card_order['project_id']},
                      "id": {"$eq": card}}}
    try:
        res = requests.get(url=url, json=body, headers=header)
        result = eval(res.text)
        return result['data']['list'][0]
    except Exception:
        raise


# def modfy_card_apply(card_apply_info):
#     creat_time = random_creat_date()
#     approve_time = random_approve_date()
#     url = 'https://api2.xlink.cn/v2/smart-parkinglot/xlink-card/apply'
#     card_apply_info['create_date'] = creat_time
#     card_apply_info['update_date'] = creat_time
#     card_apply_info['approval_time'] = approve_time
#     try:
#         res = requests.put(url=url, json=card_apply_info, headers=header)
#         result = eval(res.text)
#     except Exception:
#         raise
#     return creat_time

def get_card_info(card_apply_info, card_order):
    url = 'https://api2.xlink.cn/v2/smart-parkinglot/xlink-card/month-card/ext?data=%7B%22offset%22:0,%22limit%22:10,%22query%22:%7B%22project_id%22:%7B%22$eq%22:%22' + \
          card_order['project_id'] + '%22%7D,%22car_ids%22:%7B%22$eq%22:%5B%22' + card_apply_info['car_ids'][
              0] + '%22%5D%7D%7D,%22order%22:%7B%22create_date%22:%22desc%22%7D%7D'
    body = {"offset": 0, "limit": 10, "query": {"project_id": {"$eq": "aa748d7e3dad1df2b93fd3a7bb9f3032"},
                                                "car_ids": {"$eq": ["e9aaf8ef7d73284868592d0733dcb944"]}},
            "order": {"create_date": "desc"}}
    try:
        res = requests.get(url=url, json=body, headers=header)
        result = eval(res.text)
        return result['data']['list'][0]
    except Exception:
        raise


def modfy_card_info(card_info, creat):
    url = 'https://api2.xlink.cn/v2/smart-parkinglot/xlink-card/month-card'
    card_info['create_date'] = creat
    card_info['update_date'] = creat
    card_info['apply_date'] = creat
    try:
        res = requests.put(url=url, json=card_info, headers=header)
        result = eval(res.text)
    except Exception:
        raise


def get_renewal_date(card_order):
    url = 'https://api2.xlink.cn/v2/smart-parkinglot/xlink-card/apply/effective-date/charge'
    body = {"card_id": card_order['id'], "duration": 1}
    try:
        res = requests.post(url=url, json=body, headers=header)
        result = eval(res.text)
        return result['data']
    except Exception:
        raise


def renewal_card(month_card, new_date):
    url = 'https://api2.xlink.cn/v2/smart-parkinglot/xlink-card/apply/card-repurchase-apply'
    body = {"bill_payable": new_date['bill_payable'], "apply_mode": 1, "effective_date_begin": new_date['begin_date'],
            "effective_date_end": new_date['end_date'], "month_card_id": month_card['id']}
    try:
        res = requests.post(url=url, json=body, headers=header)
        result = eval(res.text)
        return result['data']
    except Exception:
        raise


def card_repurchase_approval(renew_id):
    url = 'https://api2.xlink.cn/v2/smart-parkinglot/xlink-card/apply/card-repurchase-approval'
    body = {"apply_id": renew_id, "approval_status": 1}
    try:
        res = requests.post(url=url, json=body, headers=header)
        result = eval(res.text)
    except Exception:
        raise


def card_repurchase_pay(card_repurchase_pay):
    url = 'https://api2.xlink.cn/v2/smart-parkinglot/xlink-card/apply/card-repurchase-pay'
    body = {"bill_payable": card_repurchase_pay['bill_payable'], "real_pay": card_repurchase_pay['bill_payable'],
            "pay_type": 10, "comment": "", "apply_mode": 1, "order_id": card_repurchase_pay['id']}
    try:
        res = requests.post(url=url, json=body, headers=header)
        result = eval(res.text)
    except Exception:
        raise


def get_card_id(car):
    url = 'https://api2.xlink.cn/v2/smart-parkinglot/xlink-card/month-card/ext?data=%7B%22offset%22:0,%22limit%22:10,%22query%22:%7B%22project_id%22:%7B%22$eq%22:%22' + \
          car['project_id'] + '%22%7D,%22car_ids%22:%0A%7B%22$eq%22:%5B%22' + car[
              'id'] + '%22%5D%7D%7D,%22order%22:%7B%22create_date%22:%22desc%22%7D%7D'
    body = {"offset": 0, "limit": 10, "query": {"project_id": {"$eq": "aa748d7e3dad1df2b93fd3a7bb9f3032"}, "car_ids":
        {"$eq": ["12700f8505bf87c69b5415f3e0c11e4a"]}}, "order": {"create_date": "desc"}}
    try:
        res = requests.get(url=url, json=body, headers=header)
        result = eval(res.text)
        return result['data']['list'][0]
    except Exception:
        raise


def get_visit_setting():
    url = 'https://api2.xlink.cn/v2/smart-access/2490b983d365adefc3f612d7921b6981/visitor/visiting-settings'
    body = {}
    try:
        res = requests.post(url=url, json=body, headers=header)
        result = eval(res.text)
        setting = result['data']['list']
        num = random.randint(0, len(setting) - 1)
        return setting[num]['id']
    except Exception:
        raise


def get_residents():
    url = 'https://api2.xlink.cn/v2/smart-access/2490b983d365adefc3f612d7921b6981/residents'
    body = {"offset": 0, "limit": 1000, "query": {"houses": {}}, "order": {"create_date": "desc"}}
    try:
        res = requests.post(url=url, json=body, headers=header)
        result = eval(res.text)
        residents = result['data']['list']
        num = random.randint(0, len(residents) - 1)
        return residents[num]
    except Exception:
        raise


def get_door():
    url = 'https://api2.xlink.cn/v2/smart-access/2490b983d365adefc3f612d7921b6981/doorlocks'
    body = {"offset": 0, "limit": 100, "query": {}, "order": {"create_date": "desc"}}
    try:
        res = requests.post(url=url, json=body, headers=header)
        result = eval(res.text)
        residents = result['data']['list']
        num = random.randint(0, len(residents) - 1)
        return residents[num]
    except Exception:
        raise


def visitor_apply():
    visit_setting = get_visit_setting()
    resident = get_residents()
    phone = RandomPhone()
    cert_id = getRandomIdCard()
    name = get_random_name()
    effective_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    expired_time = (datetime.datetime.now() + datetime.timedelta(hours=3)).strftime('%Y-%m-%d %H:%M')
    url = 'https://api2.xlink.cn/v2/smart-access/2490b983d365adefc3f612d7921b6981/visitor'
    body = {
        "open_style": 1,
        "name": name,
        "type": visit_setting,
        "phone": phone,
        "identity_number": cert_id,
        "visiting_way": 1,
        "license_plate_number": "",
        "auth_expired_time": 1,
        "face_url": "",
        "resident_name": resident['name'],
        "resident_phone": resident['phone'],
        "start": "",
        "finish": "",
        "client_type": "meidiPC",
        "employee_type": 1,
        "effective_time": effective_time,
        "customer_pay": false,
        "registrant_id": resident['id'],
        "auth_user_type_number": 1,
        "expired_time": expired_time
    }
    try:
        res = requests.post(url=url, json=body, headers=header)
        result = eval(res.text)
        return result['data']['id'], name
    except Exception:
        raise


def visitor_arrive(visitor):
    door = get_door()
    url = 'https://api2.xlink.cn/v2/smart-access/2490b983d365adefc3f612d7921b6981/open-record'
    body = {
        "device_id": door['device_id'],
        "door_lock_type": door['type'],
        "area_id": "",
        "area_name": "",
        "building_name": door['building_name'],
        "unit_id": "",
        "unit_name": "",
        "building_id": door['building_id'],
        "person_id": visitor[0],
        "person_name": visitor[1],
        "person_type": 8,
        "enter_type": "入",
        "open_time": (datetime.datetime.now() + datetime.timedelta(hours=-8)).strftime('%Y-%m-%dT%H:%M:%S.000Z'),
        "open_mode": 10,
        "person_pic": "",
        "pass_type": 1,
        "auth_resident_type": 8
    }
    try:
        res = requests.post(url=url, json=body, headers=header)
        result = eval(res.text)
        return result['data']['id']
    except Exception:
        raise


def owner_arrive():
    resident = get_residents()
    door = get_door()
    types = [1, 2, 3]
    person_type = random.choice(types)
    open_mode = [6, 8, 10]
    url = 'https://api2.xlink.cn/v2/smart-access/2490b983d365adefc3f612d7921b6981/open-record'
    body = {
        "device_id": door['device_id'],
        "door_lock_type": door['type'],
        "area_id": "",
        "area_name": "",
        "building_name": door['building_name'],
        "unit_id": "",
        "unit_name": "",
        "building_id": door['building_id'],
        "person_id": resident['id'],
        "person_name": resident['name'],
        "person_type": person_type,
        "enter_type": "入",
        "open_time": (datetime.datetime.now() + datetime.timedelta(hours=-8)).strftime('%Y-%m-%dT%H:%M:%S.000Z'),
        "open_mode": random.choice(open_mode),
        "person_pic": "",
        "pass_type": 1,
        "auth_resident_type": person_type
    }
    try:
        res = requests.post(url=url, json=body, headers=header)
        result = eval(res.text)
        XLog.GetLogger().info('住户：'+str(resident))
    except Exception:
        raise


if __name__ == '__main__':
    c_times = 2
    v_times = 10
    o_times = 200
    apply_times = []
    approve_times = []
    visitor_applies = []
    visitor_arrives = []
    owner_arrives = []
    visitors = []
    cars = []
    applys = []
    while true:
        if datetime.datetime.now().strftime('%H:%M:%S') == '06:00:00':
            visitor_applies = []
            visitor_arrives = []
            visitors = []
            time.sleep(1)
            for i in range(0, v_times):
                visitor_applies.append(random_approve_date())
                visitor_arrives.append(random_visitor_arrive_date())
            for i in range(0, o_times):
                owner_arrives.append(random_owner_arrive_date())
            XLog.GetLogger().info('visitor_applies' + str(visitor_applies))
            XLog.GetLogger().info('visitor_arrives' + str(visitor_arrives))
            XLog.GetLogger().info('owner_arrives' + str(owner_arrives))
            time.sleep(1)
        if datetime.datetime.now().strftime('%H:%M:%S') == '18:00:00':
            apply_times = []
            approve_times = []
            owns = []
            cars = []
            applys = []
            time.sleep(1)
            for i in range(0, c_times):
                apply_times.append(random_creat_date())
                approve_times.append(random_approve_date())
            XLog.GetLogger().info('apply_times:'+str(apply_times))
            XLog.GetLogger().info('strapprove_times:'+str(approve_times))
            time.sleep(1)

        # if ((datetime.datetime.now() + datetime.timedelta(hours=-8)).strftime('%Y-%m-%dT%H:%M:%S.000Z')) in apply_times:
        #     login()
        #     own = get_owner()
        #     XLog.GetLogger().info('车主：' + str(own))
        #     car = creat_car(own)
        #     XLog.GetLogger().info('车辆：' + str(car))
        #     cars.append(car)
        #     apply = card_apply(car, own)
        #     XLog.GetLogger().info('月卡申请：' + str(apply))
        #     applys.append(apply)
        # else:
        #     time.sleep(0.5)
        # if (
        # (datetime.datetime.now() + datetime.timedelta(hours=-8)).strftime('%Y-%m-%dT%H:%M:%S.000Z')) in approve_times:
        #     if len(applys) > 0:
        #         login()
        #         car_place = get_car_place()
        #         XLog.GetLogger().info('车位：' + str(car_place))
        #         effective_date = get_effective_date()
        #         card_approval(applys[0], car_place, effective_date)
        #         XLog.GetLogger().info('月卡审批')
        #         card_order = get_card_order(applys[0])
        #         pay_confirm(card_order, effective_date)
        #         XLog.GetLogger().info('月卡申请订单：' + str(card_order))
        #         month_card = get_card_id(cars[0])
        #         XLog.GetLogger().info('月卡：' + str(month_card))
        #         new_date = get_renewal_date(month_card)
        #         renew_id = renewal_card(month_card, new_date)
        #         XLog.GetLogger().info('续卡id：' + str(renew_id))
        #         card_repurchase_approval(renew_id)
        #         repurchase_pay = get_new_card_order(renew_id)
        #         card_repurchase_pay(repurchase_pay)
        #         XLog.GetLogger().info('月卡续期缴费')
        #         del applys[0]
        #         del cars[0]
        # else:
        #     time.sleep(0.5)
        if (
                (datetime.datetime.now() + datetime.timedelta(hours=-8)).strftime(
                    '%Y-%m-%dT%H:%M:%S.000Z')) in visitor_applies:
            login()
            visitor = visitor_apply()
            XLog.GetLogger().info('访客：' + str(visitor))
            visitors.append(visitor)
        else:
            time.sleep(0.5)
        if (
                (datetime.datetime.now() + datetime.timedelta(hours=-8)).strftime(
                    '%Y-%m-%dT%H:%M:%S.000Z')) in visitor_arrives:
            login()
            if len(visitors)>0:
                visitor_arrive(visitors[0])
                XLog.GetLogger().info('访客开门')
                del visitors[0]
        else:
            time.sleep(0.5)
        if (
                (datetime.datetime.now() + datetime.timedelta(hours=-8)).strftime(
                    '%Y-%m-%dT%H:%M:%S.000Z')) in owner_arrives:
            login()
            owner_arrive()
            XLog.GetLogger().info('住户开门')
        else:
            time.sleep(0.5)
