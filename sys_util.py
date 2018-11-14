import configparser


def get_sql_config(filename):
    cf = configparser.ConfigParser()
    cf.read(filename)#读取配置文件
    # 读取对应文件参数
    _host = cf.get("Database", "host")
    _port = cf.get("Database", "port")
    _database = cf.get("Database", "database")
    _user = cf.get("Database", "user")
    _pwd = cf.get("Database", "pwd")
    return _database, _host, _port, _user, _pwd


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
    c = get_sql_config("config/SQLConfig.config")
    d = get_msg_config("config/msgConfig.config")
    print (d[0])