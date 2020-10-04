'''程序逻辑配置，及第三方平台配置'''

# 赛迪云通信设置
SD_APPID = '54746'
SD_APPKEY = 'bd320103469119c56b00a678d0029bcc'
SD_PROJECT = 'QZz4V2'  # 短信模板的 ID
SD_SIGN_TYPE = 'md5'
SD_API = 'https://api.mysubmail.com/message/xsend.json'


# 七牛云配置
QN_DOMAIN = 'qh6rgg1ha.hd-bkt.clouddn.com'
QN_BUCKET = 'redzyt'
QN_ACCESS_KEY = 'SPEvoy20uKAmYxKdOtV0TVVX2xsj2EFvSNDv1o7u'
QN_SECRET_KEY = 'ZItL_NPEO_aGk0kiHHmWT9D5_XJ3tQjHIlBzyTqh'
QN_CALLBACK_URL = 'http://123.56.134.103/qiniu/callback'
QN_CALLBACK_DOMAIN = '123.56.134.103'

# Redis 配置
REDIS = {
    'host': 'localhost',
    'port': 6379,
    'db': 2,
}

# 反悔功能相关配置
REWIND_TIMES = 3         # 每日反悔次数
REWIND_TIMEOUT = 5 * 60  # 反悔超时时间
