# encoding: utf-8
import calendar
import json
import os

import datetime

import requests
import traceback

from dateutil import rrule

from common.function import find_path, get_now_date
from common import excel_unit as EX
from .login import get_host, get_login_sheet_name
from common import ini_unit as INI
from dateutil.relativedelta import relativedelta

global false, true
false = False
true = True
null = None


class Maintenance(object):
    def __init__(self):
        self.path_login = find_path() + '/data' + "/login.xlsx"
        self.path_maintenance = find_path() + '/data' + "/maintenance.xlsx"
        self.token = EX.get_key_value(self.path_login, get_login_sheet_name(), "access_token")
        self.headers = {"Content-Type": "application/json", "Access-Token": self.token}
        self.host = get_host()
        self.port = ""
        self.result = None
        self.projectid = ''

    def create_task(self):
        """创建产巡检任务，每个任务分开表格存放数据"""
        # product_id = ''
        # device_id = ''
        # point_indexs = []
        url = self.host + self.port + '/v2/service/maintenance/task'
        task_lists = EX.get_sheets(self.path_maintenance)
        product_lists = EX.load_product_data(self.path_maintenance, task_lists[0])
        for projcet in product_lists:
            project_id = self.get_project_id(projcet[0])
            self.projectid = project_id
            for task in range(1, len(task_lists)):
                base_task_body = {
                    "name": "",
                    "status": 2,
                    "project_id": "",
                    "check_items": []
                }
                check_lists = EX.load_product_data(self.path_maintenance, task_lists[task])
                for item in check_lists:
                    if item[2] != '':
                        product_id = self.get_product_id(item[2])
                        device_id = self.get_device_id(product_id, project_id,item[4])
                        points = self.get_points_lists(item[3])
                        point_indexs = self.get_data_points_indexs(product_id, points)
                    else:
                        product_id = ''
                        device_id = ''
                        point_indexs = []
                    check_items_body = self.get_check_items_json(item[0], item[1], product_id, device_id, point_indexs)
                    self.get_base_task_json(base_task_body, task_lists[task], project_id, check_items_body)
                try:
                    r = requests.post(url=url, json=base_task_body, headers=self.headers)
                    if r.status_code == 200:
                        print('[项目]' + projcet[0] + '--' + '[巡检任务]' + task_lists[task] + '巡检任务创建成功')
                        print(r.text)
                except Exception:
                    print(projcet[0] + task_lists[task] + '巡检任务创建失败！！')
                    print(traceback.format_exc())

    def create_maintenance_task(self):
        """创建巡检任务，全部任务放置在一张表格"""
        url = self.host + self.port + '/v2/service/maintenance/task'
        value_list = EX.load_data(self.path_maintenance, '巡检任务')
        task_lists = EX.load_data_by_column(self.path_maintenance, '巡检任务', '任务名称')
        project_lists = EX.load_data_by_column(self.path_maintenance, '项目信息', '项目名称')
        # 列表去重
        task_lists1 = sorted(set(task_lists), key=task_lists.index)
        for projcet in project_lists:
            project_id = self.get_project_id(projcet)
            for task in task_lists1:
                check_list = self.get_check_list(task, value_list)
                # print(check_list)
                check_items = self.get_check_items(check_list, project_id)
                # print(check_items)
                base_task_body = {
                    "name": task,
                    "status": 2,
                    "project_id": project_id,
                    "check_items": check_items
                }
                print(base_task_body)
                try:
                    r = requests.post(url=url, json=base_task_body, headers=self.headers)
                    if r.status_code == 200:
                        print('[项目]' + projcet + '--' + '[巡检任务]' + task + '巡检任务创建成功')
                        print(r.text)
                except Exception:
                    print(projcet + task + '巡检任务创建失败！！')
                    print(traceback.format_exc())

    def get_check_list(self, task_name, value_list):
        check_list = []
        for i in value_list:
            if i[2] == task_name:
                check_list.append(i)
        return check_list

    def get_check_items(self, check_list, project_id):
        # print("check_list=",check_list)
        check_items_body = []
        for item in check_list:
            # print(item)
            if item[4] != "":
                product_id = self.get_product_id(item[0])
                device_id = self.get_device_id(product_id, project_id, item[1])
                # print("device_id=",device_id)
                points = self.get_points_lists(item[3])
                point_indexs = self.get_data_points_indexs(product_id, points)
                description = item[5]
            else:
                product_id = ''
                device_id = ''
                point_indexs = []
                description = item[5]
            check_items_json = self.get_check_items_json(item[4], description, product_id, device_id, point_indexs)
            check_items_body.append(check_items_json)
            # print("check_items=", check_items_body)
        return check_items_body

    def creat_schedule(self):
        task_lists = EX.get_sheets(self.path_maintenance)
        product_lists = EX.load_product_data(self.path_maintenance, task_lists[0])
        for projcet in product_lists:
            print(projcet[0])
            project_id = self.get_project_id(projcet[0])
            # list_task = self.get_list_task(project_id)
            # day_daily_plan_id = self.creat_daily_plan(project_id,list_task,'08:30','17:30','早班')
            # night_daily_plan_id = self.creat_daily_plan(project_id,list_task,'17:30','08:30','晚班')
            day_daily_plan_id = '5d06fe89d8af2f766eda3ebb'
            night_daily_plan_id = '5d06fe8a6fb0bd7570814d6e'
            deps = self.get_project_departments(project_id)
            pos_list = self.get_project_positions(deps)
            member_list = self.get_project_members(pos_list)
            self.batch_schedule_artificial(member_list[0:3],project_id,[2019,7])
            schedule_ids = self.get_member_schedule_id(project_id, [2019, 7])
            # schedule_plans = [[1, 0, 1, 1], [1, 1, 0, 1], [2, 1, 1, 0], [0, 2, 2, 2]]
            schedule_plans = [[1, 0, 2], [2, 1, 0], [0, 2, 1]]
            for i in range(len(schedule_plans)):
                print(member_list[0:3][i])
                print(schedule_plans[i])
                self.add_member_schedule(schedule_ids, [2019, 7], day_daily_plan_id, night_daily_plan_id,
                                         schedule_plans[i], member_list[0:3][i])
            break

    def add_member_schedule(self, schedule, end_month, day_daily_plan_id, night_daily_plan_id, schedule_plan, member):
        url = ''
        now_date = self.get_now_day()
        now_month = self.get_now_month()
        end_mon = self.get_month_difference(now_month, end_month)
        for i in range(end_mon):
            if i == 0:
                a = now_date.split('-')
                mon_date = self.get_month_first_last_date(int(a[0]), int(a[1]))
                start_date = now_date
                end_date = mon_date[1]
            else:
                now_month = self.get_month(now_month, 1)
                a = now_month.split('-')
                mon_date = self.get_month_first_last_date(int(a[0]), int(a[1]))
                start_date = mon_date[0]
                end_date = mon_date[1]
            scheduleid = ''
            last_date = ''
            time_difference = self.get_time_difference(start_date, end_date)
            body = {
                "name": "",
                "date_list": [
                ],
                "check_member_id": member['check_member_id'],
                "check_member_name": member['check_member_name'],
                "status": 2
            }
            for i in range((int(time_difference / len(schedule_plan))) + 1):
                month = self.get_date_month(start_date)
                last_date = now_date
                for k in schedule:
                    if month == k['date_format'] and member['check_member_name']==k['check_member_name']:
                        scheduleid = k['schedule_id']
                        break
                url = self.host + self.port + '/v2/service/maintenance/schedule_artificial/' + scheduleid
                for j in schedule_plan:
                    data_list_dict = {
                        "date": "",
                        "daily_plan_ids": [
                        ]
                    }
                    if j == 1:
                        a = self.check_month_difference(last_date, now_date)
                        if a:
                            data_list_dict['date'] = now_date
                            data_list_dict['daily_plan_ids'].append(day_daily_plan_id)
                            body['date_list'].append(data_list_dict)
                            last_date = now_date
                            now_date = self.get_dates(now_date, 1)
                    if j == 2:
                        a = self.check_month_difference(last_date, now_date)
                        if a:
                            data_list_dict['date'] = now_date
                            data_list_dict['daily_plan_ids'].append(night_daily_plan_id)
                            body['date_list'].append(data_list_dict)
                            last_date = now_date
                            now_date = self.get_dates(now_date, 1)
                    if j == 0:
                        a = self.check_month_difference(last_date, now_date)
                        if a:
                            last_date = now_date
                            now_date = self.get_dates(now_date, 1)
            try:
                r = requests.put(url=url, json=body, headers=self.headers)
                result = eval(r.text)
                print(json.dumps(result))
                print('添加每个月成员排班设置成功')
            except Exception:
                print('添加每个月成员排班设置出错')
                print(traceback.format_exc())

    def get_member_schedule_id(self, project_id, end_months):
        member_schedule_ids = []
        now_month = self.get_now_month()
        end_mon = self.get_month_difference(now_month, end_months)
        url = self.host + self.port + '/v2/service/maintenance/list_schedule_artificial'
        for i in range(end_mon):
            body = {
                "query": {
                    "project_id": {
                        "$eq": project_id
                    },
                    "date_format": {
                        "$eq": now_month
                    }
                },
                "offset": 0,
                "limit": 1000,
                "filter": [
                    "schedule_id",
                    "name",
                    "type",
                    "project_id",
                    "date_list",
                    "check_member_id",
                    "check_member_name",
                    "status",
                    "date_format"
                ]
            }
            try:
                r = requests.post(url=url, json=body, headers=self.headers)
                result = eval(r.text)
                for i in result['data']['list']:
                    member_schedule_ids.append(
                        {"date_format": now_month, "check_member_id": i['check_member_id'],
                         "check_member_name": i['check_member_name'],
                         'schedule_id': i['schedule_id']})
                now_month = self.get_month(now_month, 1)
            except Exception:
                print('获取成员排成id出错')
                print(traceback.format_exc())
        return member_schedule_ids

    def get_now_month(self):
        now = datetime.datetime.now().strftime('%Y-%m')
        return now

    def get_now_day(self):
        now = datetime.datetime.now().strftime('%Y-%m-%d')
        return now

    def batch_schedule_artificial(self, member_list, project_id, end_months):
        now_month = self.get_now_month()
        url = self.host + self.port + '/v2/service/maintenance/batch_schedule_artificial'
        end_mon = self.get_month_difference(now_month, end_months)
        for j in range(end_mon):
            body = {
                "type": 3,
                "project_id": project_id,
                "date_format": now_month,
                "is_cover": false,
                "schedule_list": []
            }
            for i in range(len(member_list)):
                s_body = {
                    "name": "",
                    "date_list": [

                    ],
                    "check_member_id": member_list[i]['check_member_id'],
                    "check_member_name": member_list[i]['check_member_name'],
                    "status": 2
                }
                body['schedule_list'].append(s_body)
            try:
                r = requests.post(url=url, json=body, headers=self.headers)
                now_month = self.get_month(now_month, 1)
            except Exception:
                print('添加排班设置出错')
                print(traceback.format_exc())

    def creat_daily_plan(self, project_id, list_tasks, start_time, end_time, plan_name):
        url = self.host + self.port + '/v2/service/maintenance/daily_plan'
        body = {
            "name": plan_name,
            "start_time": start_time,
            "end_time": end_time,
            "project_id": project_id,
            "task_ids": list_tasks
        }
        try:
            r = requests.post(url=url, json=body, headers=self.headers)
            result = eval(r.text)
            return result['data']["daily_plan_id"]
        except Exception:
            print('添加排班设置出错')
            print(traceback.format_exc())

    def get_project_departments(self, project_id):
        url = self.host + self.port + '/v2/realty-master-data/authorizations/projects/' + project_id
        try:
            r = requests.get(url=url, headers=self.headers)
            result = eval(r.text)
            return result['data']["department_ids"]
        except Exception:
            print('获取项目部门id出错')
            print(traceback.format_exc())

    def get_project_positions(self, department_ids):
        posi_ids = []
        url = self.host + self.port + '/v2/corp/positions'
        # for i in department_ids:
        body = {
            "offset": 0,
            "limit": 1000,
            "filter": [
                "id",
                "name",
                "role_ids"
            ],
            "query": {
                "department_id": {
                    "$in": department_ids
                }
            }
        }
        try:
            r = requests.post(url=url, json=body, headers=self.headers)
            result = eval(r.text)
            for i in result['list']:
                posi_ids.append(i['id'])
            return posi_ids
        except Exception:
            print('获取项目岗位id出错')
            print(traceback.format_exc())

    def get_project_members(self, positions):
        memb_ids = []
        url = self.host + self.port + '/v2/corp/members'
        # for i in department_ids:
        body = {
            "offset": 0,
            "limit": 1000,
            "filter": [
                "id",
                "name",
                "role_ids"
            ],
            "query": {
                "position_ids": {
                    "$in": positions
                }
            }
        }
        try:
            r = requests.post(url=url, json=body, headers=self.headers)
            result = eval(r.text)
            for i in result['list']:
                memb_ids.append({"check_member_id": i['id'], "check_member_name": i['name']})
            return memb_ids
        except Exception:
            print('获取项目成员id出错')
            print(traceback.format_exc())

    def get_list_task(self, project_id):
        list_tasks_id = []
        url = self.host + self.port + '/v2/service/maintenance/list_task'
        body = {
            "query": {
                "project_id": {
                    "$eq": project_id
                },
                "status": {
                    "$eq": 2
                },
                "name": {

                }
            },
            "filter": [
                "task_id",
                "name",
                "status"
            ],
            "limit": 10,
            "offset": 0
        }
        try:
            r = requests.post(url=url, json=body, headers=self.headers)
            result = eval(r.text)
            for i in result['data']["list"]:
                list_tasks_id.append(i['task_id'])
            return list_tasks_id
        except Exception:
            print('获取巡检任务id出错')
            print(traceback.format_exc())

    def get_base_task_json(self, base_task_body, task_name, project, check_items_body):
        base_task_body["name"] = task_name
        base_task_body["project_id"] = project
        base_task_body['check_items'].append(check_items_body)

    def get_check_items_json(self, item_name, description, product_id, device_id, datapoint_indexs):
        base = {
            "name": item_name,
            "type": 2,
            "description": description,
            "datapoint_indexs": datapoint_indexs,
            "is_upload_img": false
        }
        if product_id != '':
            base["product_id"] = product_id
        if device_id != '':
            base["device_id"] = device_id
        return base

    def get_points_lists(self, points):
        p_list = []
        p = points.split(',')
        for i in p:
            p_list.append(i)
        return p_list

    def get_product_id(self, name):
        url = self.host + self.port + '/v2/products'
        try:
            r = requests.get(url=url, headers=self.headers)
            result = eval(r.text)
            for i in result:
                if name == i['name']:
                    return i['id']
        except Exception:
            print('获取产品id出错')
            print(traceback.format_exc())

    def get_device_id(self, product_id, project_id,mac):
        url = self.host + self.port + '/v2/wide-devices'
        body = {
            "filter": [
                "id",
                'mac'
            ],
            "limit": 1000,
            "offset": 0,
            "query": {
                "product_id": {
                    "$eq": product_id
                },
                "project_ids": {
                    "$eq": project_id
                }
            }
        }
        try:
            r = requests.post(url=url, json=body, headers=self.headers)
            result = eval(r.text)
            # print("result=", result)
            for i in result['list']:
                if i['mac'] in mac:
                    return i['id']
        except Exception:
            print('获取设备id出错')
            print(traceback.format_exc())

    def get_data_points_indexs(self, product_id, point_list):
        # print("product_id=",product_id)
        data_points_indexs = []
        url = self.host + self.port + '/v2/product/' + product_id + '/datapoints'
        try:
            r = requests.get(url=url, headers=self.headers)
            result = eval(r.text)
            for i in result:
                if i['field_name'] in point_list:
                    data_points_indexs.append(i['index'])
            return data_points_indexs
        except Exception:
            print('获取数据端点id出错')
            print(traceback.format_exc())

    def get_project_id(self, name):
        # print(name)
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

    def get_time_difference(self, now_date, end_date):
        a = datetime.datetime.strptime(str(now_date), "%Y-%m-%d")
        b = datetime.datetime.strptime(str(end_date), "%Y-%m-%d")
        if now_date == end_date:
            return 0
        else:
            return int(str(b - a).split(' ')[0])

    def get_dates(self, start, days):
        start_date = datetime.datetime.strptime(str(start), "%Y-%m-%d")
        next = start_date + datetime.timedelta(days=days)
        return str(str(next).split(' ')[0])

    def get_month_difference(self, now_month, end_month):
        dates = now_month.split('-')
        year = int(dates[0])
        month = int(dates[1])
        d1 = datetime.date(year, month, 1)
        d2 = datetime.date(end_month[0], end_month[1], 28)
        months = rrule.rrule(rrule.MONTHLY, dtstart=d1, until=d2).count()
        return months

    def check_month_difference(self, now, last):
        dates_now = now.split('-')
        dates_last = last.split('-')
        if dates_now[1] == dates_last[1]:
            return True
        else:
            return False

    def get_month(self, now_month, months):
        datetime_three_month_ago = datetime.datetime.strptime(str(now_month), "%Y-%m") + relativedelta(months=months)
        date = str(str(datetime_three_month_ago).split(' ')[0])
        a = date.split('-')
        return a[0] + '-' + a[1]

    def get_date_month(self, date):
        s = date.split('-')
        return s[0] + '-' + s[1]

    def get_month_first_last_date(self, year, month):
        firstdayWeekDay, monthrange = calendar.monthrange(year, month)
        firstDay = datetime.date(year=year, month=month, day=1)
        lastday = datetime.date(year=year, month=month, day=monthrange)
        return str(firstDay), str(lastday)



if __name__ == '__main__':
    pd = Maintenance()
    # pd.create_task()
    pd.create_maintenance_task()
    # pd.creat_schedule()
