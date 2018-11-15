import configparser

def get_msg_config(filename):
    cf = configparser.ConfigParser()
    cf.read(filename)  # 读取配置文件
    # 读取对应文件参数
    _url = cf.get("msg", "url")
    _account = cf.get("msg", "account")
    _password = cf.get("msg", "password")
    _service_code = cf.get("msg", "service_code")
    return _url, _account, _password, _service_code


if __name__ == '__main__':
    d = get_msg_config("config/msgConfig.config")
    print (d[0])