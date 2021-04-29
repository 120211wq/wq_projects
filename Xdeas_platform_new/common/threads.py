import inspect
import ctypes
import threading
import time
from threading import Event

from common.Convert import getLoginDataFrame, keepHeartBreakFrame, getPLCDataFrame, getPLCStatueFrame, \
    getElectorDataFrame, getPLCConfigFrame, getHotPLCConfigFrame, getHotPLCDataFrame, getHotPLCStatueFrame
from common.TCPManager import TcpManager
from common.sql import SQLManager

tlist = []
elist = []
vlist = []


def _async_raise(tid, exctype):
    """Raises an exception in the threads with id tid"""
    if not inspect.isclass(exctype):
        raise TypeError("Only types can be raised (not instances)")
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(ident):
    try:
        _async_raise(int(ident), SystemExit)
        return True
    except Exception:
        return False


def run(event, box_id, ip_addres, ip_port, box_type):
    tcp_client = TcpManager(ip_addres, ip_port)
    try:
        tcp_client.tcp_connect()
    except Exception:
        return False
    tcp_client.tcp_upload(getLoginDataFrame(str(box_id)))
    time.sleep(1)
    if box_type == 1:
        tcp_client.tcp_upload(getPLCConfigFrame(str(box_id)))
    elif box_type == 2:
        tcp_client.tcp_upload(getHotPLCConfigFrame(str(box_id)))
    plc_data = keepHeartBreakFrame(str(box_id))
    running_HeartBreak_start = time.time()
    tcp_client.tcp_upload(plc_data)
    while True:
        event.wait(20)
        if not event.isSet():
            plc_data = keepHeartBreakFrame(str(box_id))
            tcp_client.tcp_upload(plc_data)
        if event.isSet():
            print(vlist[elist.index(event)])
            if vlist[elist.index(event)]['flag'] == 2:
                upload_continue(box_id, box_type, vlist[elist.index(event)]['type'], tcp_client, event)
            if vlist[elist.index(event)]['type'] == 'plc_data':
                if box_type == 1 and vlist[elist.index(event)]['flag'] == 1:
                    plc_data = getPLCDataFrame(str(box_id), vlist[elist.index(event)]['value'])
                    tcp_client.tcp_upload(plc_data)
                elif box_type == 2 and vlist[elist.index(event)]['flag'] == 1:
                    plc_data = getHotPLCDataFrame(str(box_id), vlist[elist.index(event)]['value'])
                    tcp_client.tcp_upload(plc_data)
            elif vlist[elist.index(event)]['type'] == 'plc_state':
                if box_type == 1:
                    plc_data = getPLCStatueFrame(str(box_id), vlist[elist.index(event)]['value'][0],
                                                 vlist[elist.index(event)]['value'][1])
                    tcp_client.tcp_upload(plc_data)
                elif box_type == 2:
                    plc_data = getHotPLCStatueFrame(str(box_id), vlist[elist.index(event)]['value'][0],
                                                    vlist[elist.index(event)]['value'][1],
                                                    vlist[elist.index(event)]['value'][2])
                    tcp_client.tcp_upload(plc_data)
            elif vlist[elist.index(event)]['type'] == 'ele_data':
                if vlist[elist.index(event)]['flag'] == 1:
                    plc_data = getElectorDataFrame(str(box_id), vlist[elist.index(event)]['value'][0],
                                                   vlist[elist.index(event)]['value'][1])
                    tcp_client.tcp_upload(plc_data)
            event.clear()
            vlist[elist.index(event)] = None


def creat_box(box_id, ip_addres, ip_port, box_type):
    try:
        event = Event()
        t = threading.Thread(target=run, args=(event, box_id, ip_addres, ip_port, box_type,))
        # t.setDaemon(True)
        t.start()
        a = t.ident
        tlist.append(a)
        elist.append(event)
        vlist.append(None)
        return a
    except Exception:
        raise


def upload_continue(box_id, box_type, type, tcp_client, event):
    try:
        t = threading.Thread(target=run_continue, args=(box_type, type, tcp_client, box_id, event,))
        # t.setDaemon(True)
        t.start()
        a = t.ident
        c = SQLManager()
        if type == 'plc_data':
            sql = "update running_box set plc_con_ident = " + str(a) + " where box_number = " + box_id
            c.insert_spl(sql)
        elif type == 'ele_data':
            sql = "update running_box set ele_con_ident = " + str(a) + " where box_number = " + box_id
            c.insert_spl(sql)
    except Exception:
        raise


def run_continue(box_type, type, tcp_client, box_id, event):
    dicts = vlist[elist.index(event)]
    while True:
        if box_type == 1 and type == 'plc_data':
            plc_data = getPLCDataFrame(str(box_id), dicts['value'])
            tcp_client.tcp_upload(plc_data)
        elif box_type == 2 and type == 'plc_data':
            plc_data = getHotPLCDataFrame(str(box_id), dicts['value'])
            tcp_client.tcp_upload(plc_data)
        elif type == 'ele_data':
            plc_data = getElectorDataFrame(str(box_id), dicts['value'][0],
                                           dicts['value'][1])
            tcp_client.tcp_upload(plc_data)
        time.sleep(20)


def put_vlist(ident, type, value, flag):
    dicts = {}
    dicts['type'] = type
    dicts['value'] = value
    dicts['flag'] = flag
    if ident in tlist:
        vlist[tlist.index(ident)] = dicts
        elist[tlist.index(ident)].set()
