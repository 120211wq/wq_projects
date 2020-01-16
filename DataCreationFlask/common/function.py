# coding=utf-8

import logging,datetime
import os,re
import imaplib
import random,string


def find_path():
    '''
    返回工程所在路径
    :return:
    '''
    base_dir = os.path.dirname(os.path.dirname(__file__))
    base_dir = str(base_dir)
    base_dir = base_dir.replace('\\', '/')

    return base_dir


def find_files(path, rule):
    lists = []
    for f_path, dirs, files in os.walk(path):
        for fs in files:
            filename = os.path.join(f_path, fs)
            filename = str(filename)
            filename = filename.replace("\\", "/")
            if filename.endswith(rule):
                lists.append(filename)
    return lists


def log(massage):
    '''
    日志打印，将日志保存到report/log文件夹
    :param massage: 日志内容
    :return:
    '''
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    path = find_path() + '/report/log/'
    isexists = os.path.exists(path)
    if not isexists:
        os.makedirs(path)
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename=path+'/'+now+'.log')
    logging.info(massage)


def get_now_date():
    '''
    获取当前年月日
    :return:年-月-日
    '''
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    return now


def random_num():
    return random.randint(10000000, 99999999)


def random_string():
    return "".join(random.sample(['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i',
                                      'h','g','f','e','d','c','b','a'], 8)).replace(" ","")

def random_string_mac():
    return "".join(random.sample(['A','B','C','D','E','F','0','1','2','3','4','5','6','7','8','9'], 12)).replace(" ","")


'''
排列顺序从左至右依次为：六位数字地址码，八位数字出生日期码，三位数字顺序码和一位校验码:
1、地址码 
表示编码对象常住户口所在县(市、旗、区)的行政区域划分代码，按GB/T2260的规定执行。
2、出生日期码 
表示编码对象出生的年、月、日，按GB/T7408的规定执行，年、月、日代码之间不用分隔符。 
3、顺序码 
表示在同一地址码所标识的区域范围内，对同年、同月、同日出生的人编定的顺序号，顺序码的奇数分配给男性，偶数分配给女性。 
4、校验码计算步骤
    (1)十七位数字本体码加权求和公式 
    S = Sum(Ai * Wi), i = 0, ... , 16 ，先对前17位数字的权求和 
    Ai:表示第i位置上的身份证号码数字值(0~9) 
    Wi:7 9 10 5 8 4 2 1 6 3 7 9 10 5 8 4 2 （表示第i位置上的加权因子）
    (2)计算模 
    Y = mod(S, 11)
    (3)根据模，查找得到对应的校验码 
    Y: 0 1 2 3 4 5 6 7 8 9 10 
    校验码: 1 0 X 9 8 7 6 5 4 3 2
'''


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
    from .addr import addr
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
    phoneNum = randomPre +Number
    return phoneNum


if __name__ == '__main__':
    # driver = webdriver.Firefox()
    # driver.get("http://admin-test.xlink.io:1081/#/auth/login")
    # scream_shot(driver, 'test1/test.jpg')
    # driver.quit()
    # print(get_now_date())
    # log("打印日志测试")
    # print(find_files(r"C:\Users\Administrator\Desktop\DataCreationFlask\data",".py"))
    # print(random_string())
    days = (datetime.datetime.strptime("2019-08-20 20:10:00", "%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime("2019-08-19 20:20:00", "%Y-%m-%d %H:%M:%S")).days
    print(days)
