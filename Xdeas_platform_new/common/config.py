
from configparser import ConfigParser
#��ȡini����
def read_env(inikey,inivaluse):
        config = ConfigParser()
        config.read("../env.ini")
        convaluse=config.get(inikey,inivaluse)
        return convaluse