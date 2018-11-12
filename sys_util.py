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


if __name__ == '__main__':
    c = get_sql_config("config/SQLConfig.config")
    print (c[0])