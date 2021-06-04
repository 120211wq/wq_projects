

class FrameType:
    """帧类型"""
    # 数据帧
    DATA_FRAME = 'dc11'
    # 状态帧
    STATUS_FRAME = 'dc12'
    # 心跳帧
    HEART_FRAME = 'dc00'
    # 通知帧
    NOTICE_FRAME = 'dc20'
    # 校验位+帧尾
    TAIL_FRAME = '0000cd'
    # 配置帧
    CONFIG_FRAME = 'dc21'


class CodeType:
    """数据类型"""
    # PLC 数据
    PLC_DATA = '1d0401'
    # PLC 状态
    PLC_STATUS = '190402'
    # plc参数配置
    PCL_CONFIG = '100481'
    # 登录code
    LOGIN_CODE = '020100'
    # 离线通知
    OFFLINE_CODE = '020110'
    # 用电数据
    ELECTOR_DATA = '160301'
    # 用电异常
    ELECTOR_EXCEPTION = '040302'


class CommonFrame:
    """帧长+协议版本+模式+预留"""
    # PLC 数据 --帧长+协议版本+模式+预留，工作模式+解析规则+锅炉信息
    PLC_DATA_COMMON = '001e010200'
    # 工作模式+解析规则+锅炉长度+锅炉信息
    PLC_DATA_MODE_RULE_MSG = '00010001080001001600030007'
    # 热水锅炉工作模式+解析规则+锅炉长度+锅炉信息
    PLC_HOT_DATA_MODE_RULE_MSG = '00020001080001001600030007'
    # PLC 状态 --帧长+协议版本+模式+预留
    PLC_STATUS_COMMON = '001a010200'
    # 热水锅炉PLC 状态 --帧长+协议版本+模式+预留
    PLC_HOT_STATUS_COMMON = '0016010200'
    # plc参数配置 --帧长+协议版本+模式+预留
    PCL_CONFIG_COMMON = '0011010200'
    PLC_CONFIG_DATA = '0605006400140004000300010001'
    # 热水plc参数配置 --帧长+协议版本+模式+预留
    PLC_HOT_CONFIG_DATA = '0605006400140004000300020001'
    # 登录 --帧长+协议版本+模式+预留
    LOGIN_CODE_COMMON = '0003010200'
    # 离线通知 --帧长+协议版本+模式+预留
    OFFLINE_CODE_COMMON = '0003010200'
    # 用电数据 --帧长+协议版本+模式+预留
    ELECTOR_DATA_COMMON = '0017010200'
    # 用电异常 --帧长+协议版本+模式+预留
    ELECTOR_EXCEPTION_COMMON = '0005010200'
    # 心跳 --帧长+协议版本+模式+预留
    HEART_BREAK_COMMON = '0000010200'

