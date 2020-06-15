from time import sleep

import requests

if __name__ == '__main__':
    while True:
        with open("token.txt", "w") as f:
            url = 'http://zhsq-iot-uat-api.sunac.com.cn/v2/corp_auth'
            header = {"Content-Type": "application/json"}
            body = {
                "account": 'YC1',
                "password": "Test1234"

            }
            r = requests.post(url, json=body, headers=header)
            result = eval(r.text)
            f.write(result['access_token'])
        sleep(10)