'''程序逻辑配置，及第三方平台配置'''

REDIS = {
    'host': 'localhost',
    'port': 6379,
    'db': 2,
}



# 赛迪云通信设置
SD_APPID = '54746'
SD_APPKEY = 'bd320103469119c56b00a678d0029bcc'
SD_PROJECT = 'QZz4V2'  # 短信模板的 ID
SD_SIGN_TYPE = 'md5'
SD_API = 'https://api.mysubmail.com/message/xsend.json'

# 七牛云配置
QN_DOMAIN = 'qh6t0s64s.hd-bkt.clouddn.com'
QN_BUCKET = 'hxc37927'

QN_ACCESS_KEY = 'siTuTCCUOXuhKfzjz8r51H_1moo0Xj6W-xvH_Tx3'
QN_SECRET_KEY = '4qnxuLEAcyLUvcPqNPO9iQvH9xuBCjvOCGb3wGKi'
QN_CALLBACK_URL = 'http://qh6t0s64s.hd-bkt.clouddn.com/qiniu/callback'
QN_CALLBACK_DOMAIN = '59.110.41.9'

# 反悔功能相关的配置
REWIND_TIMES = 3         # 每日反悔次数
REWIND_TIMEOUT = 5 * 60  # 返回超时时间

