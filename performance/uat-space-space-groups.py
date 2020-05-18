import datetime
import random
import time
from urllib3 import poolmanager

import requests
from locust import HttpLocust, TaskSet, task, between
false = False
true = True
null = None

# 定义用户行为，继承TaskSet类，用于描述用户行为
# (这个类下面放各种请求，请求是基于requests的，每个方法请求和requests差不多，请求参数、方法、响应对象和requests一样的使用，url这里写的是路径)
# client.get===>requests.get
# client.post===>requests.post

def random_string_mac():
    return "".join(random.sample(['A','B','C','D','E','F','0','1','2','3','4','5','6','7','8','9'], 12)).replace(" ","")

def random_string_car():
    return "".join(random.sample(['A','B','C','D','E','F','0','1','2','3','4','5','6','7','8','9'], 5)).replace(" ","")

def get_now_date():

    now = datetime.datetime.now().strftime('%Y-%m-%d')
    return now

def get_now_time():

    now = time.strftime('%H:%M:%S',time.localtime(time.time()))
    return now

class test_task(TaskSet):
    # task装饰该方法为一个事务方法的参数用于指定该行为的执行权重。参数越大，每次被虚拟用户执行概率越高，不设置默认是1，
    @task()
    def test_upload(self):
        # 定义requests的请求头
        header = {"Content-Type":"application/json","Access-Token":'RTAwRjAzRDhGMDdGMzk5RERFNUEzRjYzMjhFRjYxRUY1NzYwQkU3QzkwMjEzRjY5OTdDRUIzNTU1RDZCRUQwMQ=='}
        url = 'http://zhsq-iot-api.sunac.com.cn/v2/space-service/space-groups'
        body = {
            "offset": 0,
            "statisticsed": false,
            "query": {
                "where": {


                },
                "logic": "and"
            },
            "limit": 100,
            "sort": {
                "create_time": "desc"
            }
        }
        # r是包含所有响应内容的一个对象
        r = self.client.post(url, json=body, headers=header)
        # 这里可以使用assert断言请求是否正确，也可以使用if判断

        assert eval(r.text)['status'] == '200'


# 这个类类似设置性能测试，继承HttpLocust
class websitUser(HttpLocust):

    # 指向一个上面定义的用户行为类
    task_set = test_task

    # 执行事物之间用户等待时间的下界，单位毫秒，相当于lr中的think time
    wait_time = between(1, 1)