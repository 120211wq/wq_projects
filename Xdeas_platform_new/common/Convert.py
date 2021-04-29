import time

from .FrameTypes import FrameType,CodeType,CommonFrame


def getData(datas,rjust):
    data = ''
    for i in datas:
        res = int_to_hex(i,rjust)
        data += res
    return data


def int_to_hex(num,rjust):
    chaDic = {10: 'a', 11: 'b', 12: 'c', 13: 'd', 14: 'e', 15: 'f'}
    hexStr = ""

    if num < 0:
        num = num + 2 ** 32

    while num >= 16:
        digit = num % 16
        hexStr = chaDic.get(digit, str(digit)) + hexStr
        num //= 16
    hexStr = chaDic.get(num, str(num)) + hexStr
    return hexStr.rjust(rjust, '0')

def getTimeStamp():
    t = time.time()
    time_stamp = int_to_hex(int(t),8)
    # print('获取当前时间戳:' + time_stamp)
    return time_stamp

def getPLCAlarm(alarm_list):
    alarm_data = ''
    for i in range(16):
        if i+1 in alarm_list:
            alarm_data += '1'
        else:
            alarm_data += '0'
    return int_to_hex(int(alarm_data[::-1],2),4)

def getElectorAlarm(alarm_list):
    alarm_data = ''
    for i in range(6):
        if i+1 in alarm_list:
            alarm_data += '1'
        else:
            alarm_data += '0'
    return int_to_hex(int(alarm_data[::-1],2),4)

def getPLCDataFrame(device,data_list):
    data = getData(data_list,4)
    time_stamp = getTimeStamp()
    dataFrame = ''
    dataFrame = dataFrame + FrameType.DATA_FRAME
    dataFrame = dataFrame + CommonFrame.PLC_DATA_COMMON
    dataFrame = dataFrame + device
    dataFrame = dataFrame + time_stamp
    dataFrame = dataFrame + CodeType.PLC_DATA
    dataFrame = dataFrame + CommonFrame.PLC_DATA_MODE_RULE_MSG
    dataFrame = dataFrame + data
    dataFrame = dataFrame + FrameType.TAIL_FRAME
    # print('获取PCL数据帧:'+dataFrame)
    return dataFrame

def getHotPLCDataFrame(device, data_list):
    data = getData(data_list, 4)
    time_stamp = getTimeStamp()
    dataFrame = ''
    dataFrame = dataFrame + FrameType.DATA_FRAME
    dataFrame = dataFrame + CommonFrame.PLC_DATA_COMMON
    dataFrame = dataFrame + device
    dataFrame = dataFrame + time_stamp
    dataFrame = dataFrame + CodeType.PLC_DATA
    dataFrame = dataFrame + CommonFrame.PLC_HOT_DATA_MODE_RULE_MSG
    dataFrame = dataFrame + data
    dataFrame = dataFrame + FrameType.TAIL_FRAME
    # print('获取PCL数据帧:'+dataFrame)
    return dataFrame

def getHotPLCStatueFrame(device, data_list, alarm_list_1,alarm_list_2):
    data = getData(data_list, 4)
    time_stamp = getTimeStamp()
    dataFrame = ''
    dataFrame = dataFrame + FrameType.STATUS_FRAME
    dataFrame = dataFrame + CommonFrame.PLC_HOT_STATUS_COMMON
    dataFrame = dataFrame + device
    dataFrame = dataFrame + time_stamp
    dataFrame = dataFrame + CodeType.PLC_STATUS
    dataFrame = dataFrame + CommonFrame.PLC_HOT_DATA_MODE_RULE_MSG
    dataFrame = dataFrame + data
    dataFrame = dataFrame + getPLCAlarm(alarm_list_1)
    dataFrame = dataFrame + getPLCAlarm(alarm_list_2)
    dataFrame = dataFrame + FrameType.TAIL_FRAME
    # print('获取PCL状态帧:' + dataFrame)
    return dataFrame

def getPLCStatueFrame(device,data_list,alarm_list):
    data = getData(data_list, 2)
    time_stamp = getTimeStamp()
    dataFrame = ''
    dataFrame = dataFrame + FrameType.STATUS_FRAME
    dataFrame = dataFrame + CommonFrame.PLC_STATUS_COMMON
    dataFrame = dataFrame + device
    dataFrame = dataFrame + time_stamp
    dataFrame = dataFrame + CodeType.PLC_STATUS
    dataFrame = dataFrame + CommonFrame.PLC_DATA_MODE_RULE_MSG
    dataFrame = dataFrame + data
    dataFrame = dataFrame + getPLCAlarm(alarm_list)
    dataFrame = dataFrame + FrameType.TAIL_FRAME
    # print('获取PCL状态帧:' + dataFrame)
    return dataFrame

def getElectorDataFrame(device,data_list,power):
    data = getData(data_list,4)
    data_power = int_to_hex(power,8)
    time_stamp = getTimeStamp()
    dataFrame = ''
    dataFrame = dataFrame + FrameType.DATA_FRAME
    dataFrame = dataFrame + CommonFrame.ELECTOR_DATA_COMMON
    dataFrame = dataFrame + device
    dataFrame = dataFrame + time_stamp
    dataFrame = dataFrame + CodeType.ELECTOR_DATA
    dataFrame = dataFrame + data
    dataFrame = dataFrame + data_power
    dataFrame = dataFrame + FrameType.TAIL_FRAME
    # print('获取用电数据帧:' + dataFrame)
    return dataFrame

def getElectorAlarmFrame(device,alarm_list):
    time_stamp = getTimeStamp()
    dataFrame = ''
    dataFrame = dataFrame + FrameType.DATA_FRAME
    dataFrame = dataFrame + CommonFrame.ELECTOR_EXCEPTION_COMMON
    dataFrame = dataFrame + device
    dataFrame = dataFrame + time_stamp
    dataFrame = dataFrame + CodeType.ELECTOR_EXCEPTION
    dataFrame = dataFrame + getElectorAlarm(alarm_list)
    dataFrame = dataFrame + FrameType.TAIL_FRAME
    # print('获取用电异常帧:' + dataFrame)
    return dataFrame

def getLoginDataFrame(device):
    time_stamp = getTimeStamp()
    dataFrame = ''
    dataFrame = dataFrame + FrameType.NOTICE_FRAME
    dataFrame = dataFrame + CommonFrame.LOGIN_CODE_COMMON
    dataFrame = dataFrame + device
    dataFrame = dataFrame + time_stamp
    dataFrame = dataFrame + CodeType.LOGIN_CODE
    dataFrame = dataFrame + FrameType.TAIL_FRAME
    # print('获取登录帧:' + dataFrame)
    return dataFrame

def getHotPLCConfigFrame(device):
    time_stamp = getTimeStamp()
    dataFrame = ''
    dataFrame = dataFrame + FrameType.NOTICE_FRAME
    dataFrame = dataFrame + CommonFrame.PCL_CONFIG_COMMON
    dataFrame = dataFrame + device
    dataFrame = dataFrame + time_stamp
    dataFrame = dataFrame + CodeType.PCL_CONFIG
    dataFrame = dataFrame + CommonFrame.PLC_HOT_CONFIG_DATA
    dataFrame = dataFrame + FrameType.TAIL_FRAME
    # print('获取PLC配置帧:' + dataFrame)
    return dataFrame

def keepHeartBreakFrame(device):
    time_stamp = getTimeStamp()
    dataFrame = ''
    dataFrame = dataFrame + FrameType.HEART_FRAME
    dataFrame = dataFrame + CommonFrame.HEART_BREAK_COMMON
    dataFrame = dataFrame + device
    dataFrame = dataFrame + time_stamp
    dataFrame = dataFrame + FrameType.TAIL_FRAME
    # print('获取心跳帧:' + dataFrame)
    return dataFrame

def getPLCConfigFrame(device):
    time_stamp = getTimeStamp()
    dataFrame = ''
    dataFrame = dataFrame + FrameType.NOTICE_FRAME
    dataFrame = dataFrame + CommonFrame.PCL_CONFIG_COMMON
    dataFrame = dataFrame + device
    dataFrame = dataFrame + time_stamp
    dataFrame = dataFrame + CodeType.PCL_CONFIG
    dataFrame = dataFrame + CommonFrame.PLC_CONFIG_DATA
    dataFrame = dataFrame + FrameType.TAIL_FRAME
    # print('获取PLC配置帧:' + dataFrame)
    return dataFrame



if __name__ == '__main__':
    a = int_to_hex(2114,4)
    print(a)
