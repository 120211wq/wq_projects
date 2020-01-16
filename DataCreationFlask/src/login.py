# coding=utf-8
import traceback

import requests
import os
from common import excel_unit as EX
from common.function import find_path

curpath = os.path.dirname(os.path.realpath(__file__))

login_sheet = "IOT"

# login_sheet = "PRO"
# login_sheet = "DEV"
# login_sheet = "私有云"

iot_api = 'https://api2.xlink.cn'
release_api = 'https://api-release-pre.xlink.cn'


def get_host(sheet=login_sheet):
    path = find_path() + '/data' + "/login.xlsx"
    host = EX.get_key_value(path, sheet, "host")
    return host


def get_login_sheet_name(sheet=login_sheet):
    return sheet


def login(sheet_name=login_sheet):
    path = find_path() + '/data' + "/login.xlsx"
    host = get_host(sheet_name)
    port = ""
    api = EX.get_key_value(path, sheet_name, "api")
    login_url = host + port + api
    username = EX.get_key_value(path, sheet_name, "username")
    password = EX.get_key_value(path, sheet_name, "password")
    data = {"account": username, "password": password}
    header = {"Content-Type": "application/json"}
    print(login_url)
    res = requests.post(login_url, json=data, headers=header)
    if res.status_code == 200:
        print("登录%s成功" % sheet_name)
    else:
        print("登录%s失败" % sheet_name)
    change_cont = eval(res.text)
    token = change_cont["access_token"]
    EX.write_key_value(path, sheet_name, "access_token", token)


def login_with_api(api_addr, user, pwd):
    path = find_path() + '/data' + "/login.xlsx"
    api = EX.get_key_value(path, get_login_sheet_name(), "api")
    if api_addr == '1':
        api_addr = iot_api
    elif api_addr == '2':
        api_addr = release_api
    login_url = api_addr + api
    data = {"account": user, "password": pwd}
    header = {"Content-Type": "application/json"}
    try:
        res = requests.post(login_url, json=data, headers=header)
        if res.status_code == 200:
            change_cont = eval(res.text)
            token = change_cont["access_token"]
            EX.write_key_value(path, get_login_sheet_name(), "host", api_addr)
            EX.write_key_value(path, get_login_sheet_name(), "access_token", token)
            return True
        else:
            return False
    except:
        print('traceback.format_exc():\n%s' % traceback.format_exc())
        return False


if __name__ == "__main__":
    login()
