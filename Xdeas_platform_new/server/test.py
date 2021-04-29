import threading
import time
import inspect
import ctypes
from datetime import datetime
from threading import Event


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
    _async_raise(ident, SystemExit)


def run(event):
    print("begin run the child thread")
    while True:
        event.wait(10)
        if not event.isSet():
            print("sleep 1s")
            # time.sleep(10)

        if event.isSet():
            print(vlist[elist.index(event)])
            event.clear()
            time.sleep(1)



if __name__ == "__main__":
    tlist = []
    elist = []
    vlist = []
    a = None
    a1 = None
    for i in range(30):
        print('mian:'+str(i))
        if i == 1:
            print("begin run main thread")
            event = Event()
            t = threading.Thread(target=run, args=(event,))
            t.setDaemon(True)
            t.start()
            a = t.ident
            tlist.append(a)
            elist.append(event)
            vlist.append(None)

            event1 = Event()
            t1 = threading.Thread(target=run, args=(event1,))
            t1.setDaemon(True)
            t1.start()
            a1 = t1.ident
            tlist.append(a1)
            elist.append(event1)
            vlist.append(None)
            print(tlist)
            print(elist)
        if i == 3:
            # _async_raise(a, SystemExit)
            vlist[tlist.index(a)] = [1,2,3]
            elist[tlist.index(a)].set()
        if i == 6:
            # _async_raise(a, SystemExit)
            vlist[tlist.index(a1)] = [2, 3, 4]
            elist[tlist.index(a1)].set()
        if i == 12:
            # _async_raise(a, SystemExit)
            vlist[tlist.index(a1)] = [3, 4, 5]
            elist[tlist.index(a1)].set()
        time.sleep(1)
    print("main thread end")

