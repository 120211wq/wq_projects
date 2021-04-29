
from configparser import ConfigParser
#∂¡»°ini∑Ω∑®
def read_env(inikey,inivaluse):
        config = ConfigParser()
        config.read("../env.ini")
        convaluse=config.get(inikey,inivaluse)
        return convaluse