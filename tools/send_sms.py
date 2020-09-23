import time
import json
from hashlib import md5

import requests



def send_sms(phone,code):
    # appid = '54746'
    appid = '1111'
    appkey = 'bd320103469119c56b00a678d0029bcc'

    args = {
        'appid': '54746',  # APPID
        'to': phone,  # 手机号
        'project': 'QZz4V2',  # 短信模板的 ID
        'vars': json.dumps({'code': code}),
        'timestamp': int(time.time()),
        'sign_type': 'md5',
    }

    api = 'https://api.mysubmail.com/message/xsend.json'

    # 计算参数的签名
    sorted_args = sorted(args.items())  # 提取每一项
    args_str = '&'.join([f'{key}={value}' for key, value in sorted_args])  # 对参数排序、组合
    sign_str = f'{appid}{appkey}{args_str}{appid}{appkey}'.encode('utf8')  # 拼接成待签名字符串
    signature = md5(sign_str).hexdigest()  # 计算签名
    args['signature'] = signature

    response = requests.post(api, data=args)
    # print('状态码：', response.status_code)

    result = response.json()
    # print('短信结果：', result)

    return result['status']
