# -*- coding:utf-8 -*-
import json
from configparser import ConfigParser

import requests

from common.sql import SQLManager

false = False
true = True
null = None

p_list = {}


def read_env(inikey, inivaluse):
    config = ConfigParser()
    config.read("../env.ini")
    convaluse = config.get(inikey, inivaluse)
    return convaluse


class ProtocolInit():
    def get_all_protocol_list(self, session, env):
        url = 'https://' + env + '/xdeas_api/xdeas-protocol-manager/v1/protocolItemType/listAll'
        headers = {"Content-Type": "application/json", 'Session-Id': session, "role": "superAdmin"}
        r = requests.get(url=url, headers=headers)
        res = eval(r.text)
        for i in res['data']:
            p_list[i['id']] = i['name']

    def get_all_protocol(self, session, env):
        self.get_all_protocol_list(session, env)
        c = SQLManager()
        url = 'https://' + env + '/xdeas_api/xdeas-protocol-manager/v1/protocolConfig/list?currentPage=1&pageSize=100'
        headers = {"Content-Type": "application/json", 'Session-Id': session, "role": "superAdmin"}
        r = requests.get(url=url, headers=headers)
        res = eval(r.text)
        for i in res['data']['data']:
            p_data = self.get_protocol_detail(i['id'], env, session)
            p_data = self.Sorting(p_data)
            p_data['code'] = str(i['code'])
            sql = "INSERT INTO protocol (name,code,data) VALUES (" + "'" + i['name'] + "'" + "," + str(
                i['code']) + ",'" + str(
                json.dumps(p_data, ensure_ascii=false)) + "')"
            c.insert_spl(sql)
            print(str(res['data']['data'].index(i)) + '/' + str(len(res['data']['data'])) + '--' + i['name'] + '入库成功')

    def get_protocol_detail(self, id, env, session):
        p = {
            'code': "",
            "01": {},
            "02": {}
        }
        alarm = {}
        url = 'https://' + env + '/xdeas_api/xdeas-protocol-manager/v1/protocolConfig/selectById?id=' + id
        headers = {"Content-Type": "application/json", 'Session-Id': session, "role": "superAdmin"}
        r = requests.get(url=url, headers=headers)
        res = eval(r.text)
        if 'protocolItemList' in res['data'].keys():
            for i in res['data']['protocolItemList']:
                if i['dataType'] == 'REALTIME_DATA':
                    if len(i['protocolItemAddressList']) == 1:
                        if i['protocolItemType'] == '':
                            p['01']['暂无类型' + str(res['data']['protocolItemList'].index(i))] = i[
                                'protocolItemAddressList']
                        else:
                            p['01'][p_list[i['protocolItemType']]] = i['protocolItemAddressList']
                    else:
                        if i['protocolItemType'] == '':
                            p['01']['暂无类型' + str(res['data']['protocolItemList'].index(i))] = i[
                                'protocolItemAddressList']
                        else:
                            p['01']['D' + p_list[i['protocolItemType']]] = i['protocolItemAddressList']
                elif i['dataType'] == 'STATUS_DATA':
                    if 'dataPosition' not in i.keys():
                        if i['protocolItemType'] == '':
                            p['01']['暂无类型' + str(res['data']['protocolItemList'].index(i))] = i[
                                'protocolItemAddressList']
                        else:
                            p['02'][p_list[i['protocolItemType']]] = i['protocolItemAddressList']
                    else:
                        alarm[i['protocolItemAddressList'][0]] = 1
            a = 1
            for i in alarm.keys():
                p['02']['锅炉故障' + str(a)] = [i]
                a += 1
        return p

    def Sorting(self,incomelist):
        sorting_01 = dict(sorted(incomelist['01'].items(), key=lambda kv1: (kv1[1], kv1[0])))
        sorting_02 = dict(sorted(incomelist['02'].items(), key=lambda kv1: (kv1[1], kv1[0])))
        incomelist['01'] = sorting_01
        incomelist['02'] = sorting_02
        return incomelist


