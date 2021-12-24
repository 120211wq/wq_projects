# -*- coding:utf-8 -*-
import random
import re
import time

import requests
import flask, json
from flask_cors import *
from common import excel_unit as EX
from flask import request
from flask_httpauth import HTTPBasicAuth
from common.TCPManager import GetTcpServerAddr
from common.config import read_env, ProtocolInit
from common.sql import SQLManager
from common.threads import creat_box, stop_thread, put_vlist
from server.user_token import create_token, verify_auth_token

server = flask.Flask(__name__)
excel_path = '../report.xlsx'
CORS(server, supports_credentials=True)
auth = HTTPBasicAuth()
server.config['JSON_SORT_KEYS'] = False

null = None


@server.route('/getAnalysis', methods=['get'])
def get_analysis():
    creat_list = EX.load_analysis_data(excel_path, 'Analysis')
    dic = {}
    dic['CPU'] = creat_list[0]
    dic['内存'] = creat_list[1]
    dic['分辨率'] = creat_list[2]
    dic['网络'] = creat_list[3]
    dic['耗时'] = creat_list[4]
    dic['CPU峰值'] = creat_list[5]
    dic['CPU均值'] = creat_list[6]
    dic['内存峰值'] = creat_list[7]
    dic['内存均值'] = creat_list[8]
    dic['电量测试之前'] = creat_list[11]
    dic['电量测试之后'] = creat_list[12]
    dic['上行流量峰值'] = creat_list[13]
    dic['上行流量均值'] = creat_list[14]
    dic['下行流量峰值'] = creat_list[15]
    dic['下行流量均值'] = creat_list[16]
    return json.dumps(dic, ensure_ascii=False)


@server.route('/getEnv', methods=['post'])
def get_env():
    if request.method == 'POST':
        data = json.loads(request.get_data())
        ip = read_env(data.get('type'), 'ip')
        port = read_env(data.get('type'), 'port')
        reg_port = read_env(data.get('type'), 'reg_port')
        return {'ip': ip, 'port': port, 'reg_port': reg_port}


@server.route('/createBox', methods=['post'])
def create_box():
    if request.method == 'POST':
        # if not verify_auth_token(request.headers['token']):
        #     return {'state': 'token验证失败'}, 502
        data = json.loads(request.get_data())
        box_num = data.get('box_num')
        box_type = data.get('box_type')
        protocol_num = data.get('protocol_num')
        env = data.get('env')
        if len(box_num) != 12:
            return {'state': "盒子编号长度必须为12位，请重新输入"}, 400
        c = SQLManager()
        sql = "select box_number from running_box where box_number = " + box_num
        value = c.sel_box(sql)
        if len(value) > 0:
            return {'state': '盒子正在模拟，请换个盒子'}, 400
        reg_ip = read_env(env, 'api')
        obj = GetTcpServerAddr()
        sql = "select box_id from register where box_id = " + box_num
        value = c.sel_box(sql)
        res = obj.register_gateway(reg_ip, box_num)
        if len(value) == 0 and res != '注册接口异常':
            tcp_server = obj.get_tcp_server(reg_ip, box_num)
            if tcp_server:
                c.register_sql(box_num, tcp_server[0], str(tcp_server[1]))
            else:
                return {'state': '获取tcp服务异常'}, 400
        elif len(value) > 0 and res != '注册接口异常':
            tcp_server = obj.get_tcp_server(reg_ip, box_num)
            if not tcp_server:
                return {'state': '获取tcp服务异常'}, 400
        else:
            return {'state': res}, 400
        ident = creat_box(box_num, tcp_server[0], tcp_server[1], int(box_type), protocol_num)
        sql = "INSERT INTO running_box (box_number,box_count,protocol_num,box_type,thread_ident,plc_con_ident,ele_con_ident,env,record_time) VALUES (" + str(
            box_num) + ",1," + str(protocol_num) + "," + str(box_type) + ',' + str(
            ident) + ",null,null,'" + env + "',DATETIME('now', 'localtime'))"
        c.insert_spl(
            sql)
        sql = "INSERT INTO running_box (box_number,box_count,protocol_num,box_type,thread_ident,plc_con_ident,ele_con_ident,env,record_time) VALUES (" + str(
            box_num) + ",1," + str(protocol_num) + "," + str(box_type) + ',' + str(
            ident) + ",null,null,'" + env + "',DATETIME('now', 'localtime'))"
        c.insert_spl(
            sql)
        return {'state': '盒子模拟成功'}, 200


@server.route('/getProtocolDetail', methods=['post'])
def get_protocol_detail():
    if request.method == 'POST':
        data = json.loads(request.get_data())
        protocol_num = data.get('protocol_num')
        c = SQLManager()
        sql = "select * from protocol where code = " + str(protocol_num)
        value = c.sel_box(sql)
        if len(value) == 0:
            return {'state': '无此协议'}, 400
        else:
            return eval(value[0][3]), 200


@server.route('/getBoxes', methods=['post'])
def get_boxes():
    if request.method == 'POST':
        # if not verify_auth_token(request.headers['token']):
        #     return {'state': 'token验证失败'}, 502
        data = json.loads(request.get_data())
        types = data.get('type')
        c = SQLManager()
        sql = "select * from running_box where box_type in" + types + "order by record_time desc"
        value = c.sel_box(sql)
        res_list = {'count': len(value), 'result': [], 'state': 200}
        for i in value:
            res = {}
            res['box_number'] = i[1]
            res['box_count'] = i[2]
            res['protocol_num'] = i[3]
            res['box_type'] = i[4]
            res['thread_ident'] = i[5]
            res['plc_con_ident'] = i[6]
            res['ele_con_ident'] = i[7]
            res['env'] = i[8]
            res['record_time'] = i[9]
            res_list['result'].append(res)
        return res_list


@server.route('/stopBox', methods=['post'])
def stop_box():
    if request.method == 'POST':
        # if not verify_auth_token(request.headers['token']):
        #     return {'state': 'token验证失败'}, 502
        data = json.loads(request.get_data())
        ident = data.get('ident')
        c = SQLManager()
        sql = "select plc_con_ident, ele_con_ident from running_box where thread_ident =" + str(ident)
        value = c.sel_box(sql)
        print(value)
        for i in value[0]:
            stop_thread(i)
        res = stop_thread(ident)
        if res:
            sql = "delete from running_box where thread_ident =" + ident
            c.insert_spl(sql)
            return {'state': '线程停止成功'}, 200
        else:
            return {'state': '线程停止失败'}, 400


@server.route('/stopContinue', methods=['post'])
def stop_continue():
    if request.method == 'POST':
        # if not verify_auth_token(request.headers['token']):
        #     return {'state': 'token验证失败'}, 502
        data = json.loads(request.get_data())
        box_id = data.get('box_id')
        stop_ident = data.get('stop_ident')
        type = data.get('type')
        res = stop_thread(stop_ident)
        c = SQLManager()
        if type == 'plc_data' and res:
            sql = "update running_box set plc_con_ident = null where box_number =" + str(box_id)
            print(sql)
            c.insert_spl(sql)
        if type == 'ele_data' and res:
            sql = "update running_box set ele_con_ident = null where box_number =" + str(box_id)
            print(sql)
            c.insert_spl(sql)
        if not res:
            return {'state': '线程停止失败'}, 400
        else:
            return {'state': '线程停止成功'}, 200


@server.route('/uploadData', methods=['post'])
def upload_Data():
    res = ''
    if request.method == 'POST':
        # if not verify_auth_token(request.headers['token']):
        #     return {'state': 'token验证失败'}, 502
        data = json.loads(request.get_data())
        ident = data.get('ident')
        data_type = data.get('type')
        value = data.get('value')
        flag = data.get('flag')
        custom_type = data.get('custom_type')
        if len(value) == 0:
            return {'state': "上报数据不能为空"}, 400
        put_vlist(ident, data_type, value, flag, custom_type)
        time.sleep(1)
        if flag == 2:
            c = SQLManager()
            if data_type == 'plc_data':
                sql = "select plc_con_ident from running_box where thread_ident = " + str(ident)
                res = c.sel_box(sql)
            if data_type == 'ele_data':
                sql = "select ele_con_ident from running_box where thread_ident = " + str(ident)
                res = c.sel_box(sql)
        return {'state': '数据发送成功', "ident": res}, 200


@server.route('/login', methods=['post'])
def login():
    if request.method == 'POST':
        data = json.loads(request.get_data())
        username = data.get('username')
        password = data.get('password')
        c = SQLManager()
        sql = "select * from account where username = '" + str(username) + "'"
        res = c.sel_box(sql)
        if len(res) > 0:
            if res[0][2] == password:
                return {"state": '登录成功', 'token': create_token(username)}, 200
            else:
                return {"state": "密码错误"}, 400
        else:
            return {"state": "无此账号"}, 400


@server.route('/init', methods=['post'])
def init():
    if request.method == 'POST':
        data = json.loads(request.get_data())
        env = data.get('env')
        api = read_env(env, 'api')
        obj = GetTcpServerAddr()
        session = obj.get_xdeas_platform_session(api)
        c = SQLManager()
        sql = "delete from running_box"
        sql1 = "delete from protocol"
        c.insert_spl(sql1)
        c.insert_spl(sql)
        ProtocolInit().get_all_protocol(session, api)
    return {'state': '初始化成功'}, 200


@server.route('/getProtocolList', methods=['GET'])
def protocol_list():
    if request.method == 'GET':
        # if not verify_auth_token(request.headers['token']):
        #     return {'state': 'token验证失败'}, 502
        c = SQLManager()
        sql = "select * from protocol "
        value = c.sel_box(sql)
        res_list = {'count': len(value), 'result': [], 'state': 200}
        for i in value:
            res = {}
            res['name'] = i[1]
            res['code'] = i[2]
            res_list['result'].append(res)
        return res_list


@server.route('/getTestResource', methods=['post'])
def get_test_resource():
    if request.method == 'POST':
        c = SQLManager()
        data = json.loads(request.get_data())
        pid = data.get('p_id')
        if pid == '':
            sql = "select * from test_resource "
        else:
            sql = "select * from test_resource where id = '" + pid + "'"
        value = c.sel_box(sql)
        res_list = {'count': len(value), 'result': [], 'state': 200}
        for i in value:
            res = {}
            res['id'] = i[0]
            res['name'] = i[1]
            if i[2] == 1:
                res['code'] = '手机'
            else:
                res['code'] = '未知'
            if i[3] == 0:
                res['status'] = '可用'
            else:
                res['status'] = '已借出'
            res_list['result'].append(res)
        return res_list


@server.route('/getResourceRecord', methods=['post'])
def get_resource_record():
    if request.method == 'POST':
        data = json.loads(request.get_data())
        pid = data.get('p_id')
        c = SQLManager()
        sql = "select * from test_resource_record where p_id = '" + pid + "' order by borrow_data desc"
        value = c.sel_box(sql)
        res_list = {'count': len(value), 'result': [], 'state': 200}
        for i in value:
            res = {}
            res['pid'] = i[1]
            res['borrower'] = i[2]
            res['borrow_data'] = i[3]
            res['revert_date'] = i[4]
            res_list['result'].append(res)
        return res_list


@server.route('/addResourceRecord', methods=['post'])
def add_resource_record():
    if request.method == 'POST':
        data = json.loads(request.get_data())
        pid = data.get('p_id')
        borrower = data.get('borrower')
        c = SQLManager()
        sql = "select * from test_resource_record where p_id = '" + pid + "' order by borrow_data desc limit 1"
        value = c.sel_box(sql)
        print(value)
        if len(value)>0:
            if not value[0][4]:
                return {'state': '仍未归还，不可借出'}, 500
        sql = "INSERT INTO test_resource_record (p_id,borrower,borrow_data) VALUES ('" + str(
            pid) + "','" + str(borrower) + "',DATETIME('now', 'localtime'))"
        c.insert_spl(
            sql)
        sql = "update test_resource set status = 1 where id ='" + str(pid)+"'"
        c.insert_spl(sql)
        return {'state': '记录添加成功'}, 200

@server.route('/returnResource', methods=['post'])
def return_resource():
    if request.method == 'POST':
        data = json.loads(request.get_data())
        pid = data.get('p_id')
        c = SQLManager()
        sql = "select * from test_resource_record where p_id = '" + pid + "' order by borrow_data desc limit 1"
        value = c.sel_box(sql)
        print(value)
        if len(value) > 0:
            if value[0][4]:
                return {'state': '已归还，无需再还'}, 500
        sql = "update test_resource_record set revert_date = DATETIME('now', 'localtime') where id = "+str(value[0][0])
        c.insert_spl(
            sql)
        sql = "update test_resource set status = 0 where id ='" + str(pid) + "'"
        c.insert_spl(sql)

        return {'state': '归还成功'}, 200


if __name__ == '__main__':
    server.run(port=5200, debug=True, host='0.0.0.0', threaded=True)
