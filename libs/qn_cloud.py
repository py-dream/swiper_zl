import time
import json
from qiniu import Auth
from swiper_zl import config as cfg


def get_res_url(filename):
    '''获取资源url'''
    return f'http://{cfg.QN_DOMAIN}/{filename}'


def get_token(uid,filename):

    policy = {
        'scope' : cfg.QN_BUCKET,
        'deadline' : int(time.time() + 600),
        'returnBody' : json.dumps({'code':0,'data':get_res_url(filename)}),
        'callbackUrl' : cfg.QN_CALLBACK_URL,
        'callbackHost' : cfg.QN_CALLBACK_DOMAIN,
        'callbackBody' : f'key={filename}&uid={uid}',
        'saveKey':filename,
        'forceSaveKey':True,
        'fsizeLimit':10485760,
        'mimeLime':'image/*',
    }


    qn_auth = Auth(cfg.QN_ACCESS_KEY,cfg.QN_SECRET_KEY)

    token = qn_auth.upload_token(cfg.QN_BUCKET,filename,600,policy=policy)
    return token
