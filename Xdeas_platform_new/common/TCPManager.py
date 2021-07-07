import json
from socket import *

import requests

false = False
true = True
null = None


class TcpManager():

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.tcp_client_socket = None

    def tcp_connect(self):
        self.tcp_client_socket = socket(AF_INET, SOCK_STREAM)
        self.tcp_client_socket.connect((self.ip, self.port))
        print('已连接tcp服务')

    def tcp_upload(self, data):
        self.tcp_client_socket.send(bytearray.fromhex(data))
        # print('已发送指令')
        print(data)
        return 1

    def tcp_shutdown(self):
        self.tcp_client_socket.close()


class GetTcpServerAddr():

    def __init__(self):
        pass

    def register_gateway(self,api,number):
        url = 'https://'+api + '/xdeas-devices/insertGateway'
        print(url)
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            'name': 'test'+str(number),
            'nick_name': 'test',
            'protocol': '01',
            'number': number
        }
        r = requests.post(url=url, data=data, headers=headers)
        res = eval(r.text)
        if r.status_code == 200:
            print('注册网关成功')
            return '注册网关成功'
        elif "iot终端已存在" in res['message']:
            print(res['message'])
            return '该盒子已注册'
        else:
            print(res['message'])
            return '注册接口异常'

    def get_tcp_server(self,api,number):
        url = 'https://'+api + '/xdeas-devices/gatewayToken?number=' + str(number)
        headers = {"Content-Type": "text/plain"}
        r = requests.get(url=url, headers=headers)
        res = r.text
        if ':' in res:
            print('获取tcp服务地址成功')
            api = res.split('-')[1].split(':')
            return api[0], int(api[1])
        else:
            print(res)
            return False

    def get_xdeas_platform_session(self,api):
        url = 'http://' + api + '/xdeas_api/xdeas-user-admin/account/terminal/loginByAccount'
        headers = {"Content-Type": "application/json;charset=UTF-8"}
        body = {"mobile":"13788888888","password":"123456","account":"13788888888"}
        r = requests.post(url=url, json=body,headers=headers)
        res = eval(r.text)
        if r.status_code == 200:
            return res['data']['sessionId']
        else:
            return False

if __name__ == '__main__':
    c = GetTcpServerAddr()
    c.get_tcp_server('39.106.103.40:8769','521420911212')
