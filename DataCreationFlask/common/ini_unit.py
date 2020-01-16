# coding = utf-8
from common.myconfigparser import MyConfigParser
from common.function import find_path,get_now_date


path = find_path() + '/data' + '/devices_online'+ get_now_date() + '.ini'
cf = MyConfigParser()


def get_from_ini(fpath, section, option):
    cf.read(fpath)
    value = cf.get(section, option)
    return value


def write_to_ini(section, option, name, fpath=path):
    try:
        cf.read(fpath)
        tem = cf.has_section(section)
        if not tem:
            cf.add_section(section)
            cf.set(section, option, name)
            cf.write(open(fpath, "w"))
        else:
            cf.set(section, option, name)
            cf.write(open(fpath, "w"))
    except Exception as msg:
        print(msg)

if __name__ == '__main__':
    write_to_ini("DEVICE4", "PRODUCTNAME" ,"xiaofangwenyaben")
    # print(get_from_ini(path, "DEVICE1", "PRODUCTNAME"))
    # cf.read(path)
    # print(cf.has_section("DEVICE1"))

