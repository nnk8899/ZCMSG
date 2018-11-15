from urllib import request
# from urllib import parse
import ssl
import json
import sys_msg


def send_msg(content, mobile):
    d = sys_msg.get_msg_config("config/msgConfig.config")
    content = content
    mobile = mobile
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip,deflate,br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    }
    data = {
        "meta":
            {
                "account": d[1],
                "password": d[2],
                "service_code": d[3]
            },
        "params":
            {
                "content": content,
                "mobile": mobile
            }
    }
    ssl._create_default_https_context = ssl._create_unverified_context
    # data = parse.urlencode(data).encode('utf-8')
    data = json.dumps(data)
    data = bytes(data, 'utf8')
    url = d[0]
    req = request.Request(url=url, headers=headers, data=data)
    page = request.urlopen(req).read()
    page = page.decode('utf-8')
    p = eval(page)
    result_code = p['meta']['result_code']
    # print(page)
    return result_code


if __name__ == '__main__':
    content = "【中新水滴】欢迎使用水滴金融，贵公司的领取码为 1005,此领取码用于注册水滴供应链金融移动端账号。点击 点击 https://api.scf.chinaftg.com/img/qr.jpg 进行扫 进行扫码注册。"
    mobile = "18084800975"
    #status = send_msg(content, mobile)