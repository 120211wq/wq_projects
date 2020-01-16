# coding=utf-8
import requests
import traceback
from DataCreationFlask.common.function import find_path
from DataCreationFlask.common import excel_unit as EX
from DataCreationFlask.src.login import get_host, get_login_sheet_name

global false, true
false = False
true = True
null = None


class EquipmentAlarm(object):

    def __init__(self):
        self.path_alarm = find_path() + '/data' + '/alarm.xlsx'
        self.path_login = find_path() + '/data' + '/login.xlsx'
        self.value_list = EX.load_data(self.path_alarm, "告警规则")
        self.token = EX.get_key_value(self.path_login, get_login_sheet_name(), "access_token")
        self.headers = {"Content-Type": "application/json", "Access-Token": self.token, "Api-Version": "2"}
        self.host = get_host()
        self.port = ""

    def add_equipment_alarm(self):
        """
        添加设备告警
        :return:
        """

        for i in range(len(self.value_list)):
            product_name = self.value_list[i][0]
            category = self.get_category_id(self.value_list[0][11])
            product_id = self.get_product_id(product_name, category)
            # print(product_id)
            notify_target = self.get_tag_id(self.value_list[i][2])
            project_id = self.get_project_id(self.value_list[i][9])
            param = self.get_dp_id(self.value_list[i][6], product_id)
            compare = self.get_compare(self.value_list[i][7])

            # 添加开发平台告警规则
            # url = self.host + '/v2/alert/rule'
            # 添加项目管理告警规则
            url = self.host + '/v2/realty-master-data/projects/' + project_id + '/alert/rule'
            body = {
                "product_id": product_id,
                "deviceOnline": "online",
                "content": self.value_list[i][3],
                "name": self.value_list[i][1],
                "tag": "",
                "type": 1,
                "notify_target": [3],
                "notify_type": 2,
                "scope": 1,
                "notify_apps": [],
                "is_enable": true,
                "param": param,
                "compare": compare,
                "value": self.value_list[i][8],
                "source": 2,
                "exception": {
                    "tag_id": notify_target,
                    "suggestions": self.value_list[i][4]
                },
                "notification": {
                    "is_enable": 0,
                    "conditions": {
                        "times": self.value_list[i][5]
                    },
                    "scope": {
                        "member": {
                            "is_all": 1,
                            "department_ids": [],
                            "position_ids": [],
                            "member_ids": []
                        }
                    }
                }
            }
            # print(url)
            print(body)
            print("project_name=",self.value_list[i][9])
            try:
                r = requests.post(url=url, json=body, headers=self.headers)
                result = eval(r.text)
                # print(result)
                if "error" in result['data']:
                    print(product_name + self.value_list[i][1] + "添加告警失败", result['data'])
                else:
                    print(product_name + self.value_list[i][1] + "添加告警成功")
            except Exception:
                print('traceback.format_exc():\n%s' % traceback.format_exc())
                raise


    def device_reference(self):
        """
        增加异常告警规则引用,用于项目管理下的告警规则
        :return:
        """
        for j in range(len(self.value_list)):
            product_name = self.value_list[j][0]
            category = self.get_category_id(self.value_list[0][11])
            product_id = self.get_product_id(product_name, category)
            project_id = self.get_project_id(self.value_list[j][9])
            # device_id = self.get_device_ids(product_id, project_id, self.value_list[j][10])
            rule_id = self.get_rules_ids(product_id, project_id, self.value_list[j][1])
            compare = self.get_compare(self.value_list[j][7])
            param = self.get_dp_id(self.value_list[j][6], product_id)
            # print(project_id, rule_id)
            url = self.host + '/v2/realty-master-data/projects/' + project_id + '/alert/rule/' + rule_id + '/reference/device'
            if self.value_list[j][10] != 0:
                device_id = self.get_device_ids(product_id, project_id, self.value_list[j][10])
            else:
                device_id = self.query_devices(product_id,project_id)
            body = {
                "device_ids": device_id,
                "exception_enabled": true,
                "notification_enabled": true,
                "exception": {
                    "conditions": [{
                        "param": param,
                        "compare": compare,
                        "value": self.value_list[j][8]
                    }]
                },
                "notification": {
                    "scope": 1,
                    "push_interval": 0,
                    "conditions": {
                        "times": self.value_list[j][5],
                        "durations": 0,
                        "type": 0
                    },
                    "member": {
                        "is_all": true,
                        "member_ids": [],
                        "department_ids": [],
                        "position_ids": []
                    },
                    "way": {
                        "categorys": [3],
                        "apps": []
                    }
                }
            }
            print(url)
            print(body)
            try:
                r = requests.post(url=url, json=body, headers=self.headers)
                result = eval(r.text)
                print(result)
                if r.status_code == 200:
                    print(product_name + "设备引用成功")
                else:
                    print(product_name + "设备引用失败", r.status_code)
            except Exception:
                print('traceback.format_exc():\n%s' % traceback.format_exc())
                raise

    def get_category_id(self, name):
        """获取产品分类id"""
        lists = []
        try:
            url = self.host + self.port + '/v2/product_categories'
            r = requests.get(url=url, headers=self.headers)
            result = eval(r.text)
            # print(result)
            for i in result:
                if name == i['name']:
                    lists.append(i['id'])
        except Exception:
            print('traceback.format_exc():\n%s' % traceback.format_exc())
            raise
        return lists

    def get_product_id(self, name, category=None):
        # print(category)
        # print(name)
        url = self.host + self.port + '/v2/products?filter=total_device'
        # print(url)
        try:
            r = requests.get(url=url, headers=self.headers)
            result = eval(r.text)
            # print(result)
            for i in result:
                # print(i)
                # print(category)
                if category != []:
                    if i['name'] == name and i['categories'] == category:
                        return i['id']
                else:
                    if i['name'] == name:
                        # print(i['name'])
                        return i['id']
        except Exception:
            print('获取产品id出错')
            print(traceback.format_exc())

    def get_tag_id(self, tag_name):
        url = self.host + self.port + '/v2/exception/tags'
        try:
            r = requests.get(url=url, headers=self.headers)
            result = eval(r.text)
            for i in result['list']:
                if i['name'] == tag_name:
                    return i['id']
        except Exception:
            print('获取异常标签id出错')
            print(traceback.format_exc())

    def get_dp_id(self, tag_name, product_id):
        url = self.host + self.port + '/v2/product/' + product_id + '/datapoints'
        try:
            r = requests.get(url=url, headers=self.headers)
            result = eval(r.text)
            # print(result)
            for i in result:
                if i['field_name'] == tag_name:
                    return i['id']
        except Exception:
            print('获取数据端点id出错')
            print(traceback.format_exc())

    def get_project_id(self, name):
        url = self.host + self.port + '/v2/realty-master-data/authorizations/projects?project_type=0'
        body = {
            "limit": 10,
            "offset": 0,
            "query": {
                "name": {
                    "$like": name
                }
            }
        }
        try:
            r = requests.post(url=url, json=body, headers=self.headers)
            result = eval(r.text)
            # print(result)
            return result['data']["list"][0]['id']
        except Exception:
            print('获取项目id出错')
            print(traceback.format_exc())

    def get_device_ids(self, product_id, project_id, macs):
        mac = []
        device_ids = []
        if ',' in macs:
            a = macs.split(',')
            for i in a:
                mac.append(i)
        else:
            mac.append(macs)
        url = self.host + self.port + '/v2/realty-master-data/authorizations/projects/devices'
        body = {
            "filter": [
                "id",
                "mac",
                "name",
                "sn",
                "product_id"
            ],
            "limit": 100,
            "offset": 0,
            "query": {
                "device": {
                    "product_id": {
                        "$in": [
                            product_id
                        ]
                    }
                },
                "master": {
                    "project_id": {
                        "$eq": project_id
                    }
                }
            }
        }
        try:
            r = requests.post(url=url, json=body, headers=self.headers)
            result = eval(r.text)
            for i in result['data']['list']:
                if i['mac'] in mac:
                    device_ids.append(i['id'])
            return device_ids
        except Exception:
            print('获取设备id出错')
            print(traceback.format_exc())

    def query_devices(self, pid,projec_id):
        """
        查询设备
        :return: 设备id
        """
        devices_id = []
        url = self.host + self.port + '/v2/realty-master-data/authorizations/projects/devices'
        data = {
            "filter":[
                "id",
                "mac",
                "name",
                "sn",
                "product_id"
            ],
            "limit":10,
            "offset":0,
            "query":{
                "device":{
                    "product_id":{
                        "$in":[
                            pid
                        ]
                    }
                },
                "master":{
                    "project_id":{
                        "$eq":projec_id
                    }
                }
            }
        }
        # 查询设备列表
        try:
            r = requests.post(url=url, json=data, headers=self.headers)
            if (r.status_code == 200):
                print("查询设备成功")
                res = eval(r.text)
                # 获取设备id
                for i in range(res['data']['count']):
                    devices_id.append(res['data']['list'][i]['id'])
            else:
                print("查询失败：", r.status_code)

        except Exception:
            print('traceback.format_exc():\n%s' % traceback.format_exc())
            raise
        return devices_id

    def get_rules_ids(self, product_id, project_id, rules_name):
        url = self.host + self.port + '/v2/realty-master-data/projects/'+project_id+'/alert/rules'
        body = {

            "filter": [
                "product_id"
            ],
            "limit": 1000,
            "offset": 0,
            "query": {

                "product_id": {
                    "$in": [
                        product_id
                    ]
                }

            }
         }
        try:
            r = requests.post(url=url, json=body, headers=self.headers)
            result = eval(r.text)
            # print(result)
            for i in result['data']['list']:
                if i['name'] == rules_name:
                    return i['id']
        except Exception:
            print('获取规则id出错')
            print(traceback.format_exc())

    def get_compare(self, compare):
        try:
            if compare != "":
                for i in range(len(self.value_list)):
                    # 判断规则比较类型
                    if compare == u'等于':
                        compare = 1
                    elif compare == u'大于':
                        compare = 2
                    elif compare == u'小于':
                        compare = 3
                    elif compare == u'大于等于':
                        compare = 4
                    elif compare == u'小于等于':
                        compare = 5
                    elif compare == u'不等于':
                        compare = 6
                return compare
            else:
                print('获取条件失败')
        except Exception:
            print(traceback.format_exc())


if __name__ == "__main__":
    alarm = EquipmentAlarm()
    # alarm.add_equipment_alarm()
    alarm.device_reference()


