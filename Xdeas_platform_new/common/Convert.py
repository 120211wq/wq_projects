import decimal
import struct
import time

# from .FrameTypes import FrameType,CodeType,CommonFrame
from common.FrameTypes import FrameType, CommonFrame, CodeType


def getData(datas, rjust):
    data = ''
    for i in datas:
        res = int_to_hex(i, rjust)
        data += res
    return data


def getCustomData(datas, type):
    addrs = []
    data = ''
    if type == '01':
        for i in datas[type].keys():
            if ',' not in datas[type][i]:
                addrs.append(datas[type][i])
            else:
                splits = datas[type][i].split(',')
                for j in splits:
                    addrs.append(j)
    if type == '02':
        for i in datas[type]['status'].keys():
            if ',' not in datas[type]['status'][i]:
                addrs.append(datas[type]['status'][i])
            else:
                splits = datas[type]['status'][i].split(',')
                for j in splits:
                    addrs.append(j)
        for i in datas[type]['alarm'].keys():
            if ',' not in datas[type]['alarm'][i]:
                addrs.append(datas[type]['alarm'][i])
            else:
                splits = datas[type]['alarm'][i].split(',')
                for j in splits:
                    addrs.append(j)
    for i in addrs:
        res = int_to_hex(int(i[1:5]) - 1, 4)
        if i[0] == '4':
            data += ('03' + res)
    return data


def getCustomPlcData(datas):
    # data_list = []
    data = ''
    for i in datas.keys():
        if 'D' in i:
            res = float_to_hex(datas[i][0])
            data += res
        elif '锅炉故障' in i:
            res = getPLCAlarm(datas[i])
            data += res
        else:
            res = int_to_hex(datas[i][0], 4)
            data += res
    return data


def int_to_hex(num, rjust):
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
    time_stamp = int_to_hex(int(t), 8)
    # print('获取当前时间戳:' + time_stamp)
    return time_stamp


def getPLCAlarm(alarm_list):
    alarm_data = ''
    for i in range(16):
        if i + 1 in alarm_list:
            alarm_data += '1'
        else:
            alarm_data += '0'
    return int_to_hex(int(alarm_data[::-1], 2), 4)


def getElectorAlarm(alarm_list):
    alarm_data = ''
    for i in range(6):
        if i + 1 in alarm_list:
            alarm_data += '1'
        else:
            alarm_data += '0'
    return int_to_hex(int(alarm_data[::-1], 2), 4)


def getDataLen(data):
    data_list = []
    for i in data.keys():
        if ',' not in data[i]:
            data_list.append(data[i])
        else:
            splits = data[i].split(',')
            for j in splits:
                data_list.append(j)
    return len(data_list)


def float_to_hex(f):
    return hex(struct.unpack('<I', struct.pack('<f', f))[0])[2:10]


def hex_to_float(h):
    D = decimal.Decimal
    return round(D(struct.unpack('!f', bytes.fromhex(h))[0]), 5)


def get_length(data):
    a = 0
    for i in data.keys():
        if 'D' in i:
            a += 2
        else:
            a += 1
    return a


def getPLCDataFrame(device, data_list):
    data = getData(data_list, 4)
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


def getHotPLCStatueFrame(device, data_list, alarm_list_1, alarm_list_2):
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


def getPLCStatueFrame(device, data_list, alarm_list):
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


def getElectorDataFrame(device, data_list, power):
    data = getData(data_list, 4)
    data_power = int_to_hex(power, 8)
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


def getElectorAlarmFrame(device, alarm_list):
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


# def setCustomProtocolFrame(device, data, type):
#     time_stamp = getTimeStamp()
#     dataFrame = ''
#     dataFrame = dataFrame + FrameType.CONFIG_FRAME
#     if type == '01':
#         dataFrame = dataFrame + int_to_hex(getDataLen(data[type]) * 3 + 10, 4)
#     if type == '02':
#         dataFrame = dataFrame + int_to_hex(
#             (getDataLen(data[type]['status']) + getDataLen(data[type]['alarm'])) * 3 + 10, 4)
#     dataFrame = dataFrame + '010100'
#     dataFrame = dataFrame + device
#     dataFrame = dataFrame + time_stamp
#     if type == '01':
#         dataFrame = dataFrame + int_to_hex(getDataLen(data[type]) * 3 + 9, 2)
#     if type == '02':
#         dataFrame = dataFrame + int_to_hex((getDataLen(data[type]['status']) + getDataLen(data[type]['alarm'])) * 3 + 9,
#                                            2)
#     dataFrame = dataFrame + '0483' + int_to_hex(int(data['role']), 4) + type + '00000000'
#     dataFrame = dataFrame + getCustomData(data, type)
#     dataFrame = dataFrame + FrameType.TAIL_FRAME
#     return dataFrame


def getCustomProtocolFrame(device, data, type):
    time_stamp = getTimeStamp()
    dataFrame = ''
    dataFrame = dataFrame + FrameType.DATA_FRAME
    dataFrame = dataFrame + int_to_hex(get_length(data[type]) * 2 + 8, 4)
    dataFrame = dataFrame + '010200'
    dataFrame = dataFrame + device
    dataFrame = dataFrame + time_stamp
    dataFrame = dataFrame + int_to_hex(get_length(data[type]) * 2 + 7, 2)
    dataFrame = dataFrame + '04030010' + int_to_hex(int(data['code']), 4) + type
    dataFrame = dataFrame + getCustomPlcData(data[type])
    dataFrame = dataFrame + FrameType.TAIL_FRAME
    return dataFrame


def getCustomConfigFrame(device, data):
    time_stamp = getTimeStamp()
    dataFrame = ''
    dataFrame = dataFrame + FrameType.NOTICE_FRAME
    dataFrame = dataFrame + '0015010200'
    dataFrame = dataFrame + device
    dataFrame = dataFrame + time_stamp
    dataFrame = dataFrame + '140481060700640014000400030010' + int_to_hex(int(data), 4) + '00000000'
    dataFrame = dataFrame + FrameType.TAIL_FRAME
    return dataFrame


# if __name__ == '__main__':
#     a = {
#         'code': '4',
#         '01': {
#             'D本体烟温': '40430,40431',
#             '节能器后烟温': '40431',
#             '压力': '40432'
#         },
#         '02': {
#             'status': {
#                 '锅炉状态': '40437,40437',
#                 '水位状态': '40438',
#                 '压力状态': '40439',
#                 '补水泵个数': '40440',
#                 '一号泵状态': '40441',
#                 '二号泵状态': '40442',
#                 '循环泵': '40443',
#                 '循环泵状态': '40444'
#             },
#             'alarm': {
#                 '锅炉故障': '40445'
#             }
#         }
#     }
#     b = {
#         'role': '1',
#         '01': {
#             '本体烟温': [1],
#             'D节能器后烟温': [2.1],
#             '压力': [3]
#         },
#         '02': {
#             '锅炉状态': [0],
#             '水位状态': [1],
#             '压力状态': [2],
#             '补水泵个数': [3],
#             '一号泵状态': [4],
#             '二号泵状态': [5],
#             '锅炉故障': [1, 2],
#             '循环泵': [6],
#             '循环泵状态': [7]
#
#         }
#     }
#
#     # print(setCustomProtocolFrame('510120120091',a,'01'))
#     # print(setCustomProtocolFrame('510120120091', a, '02'))
#     print(getCustomProtocolFrame('510120120091', b, '01'))
#     print(getCustomProtocolFrame('510120120091', b, '02'))
#     print(getCustomConfigFrame('522122136950', 4))
