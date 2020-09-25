from django.http import JsonResponse
from django.core.cache import cache

from libs.qn_cloud import gen_token, get_res_url
from user.forms import UserForm, ProfileForm
from user.logics import send_vcode
from user.models import User, Profile


def fetch_vcode(request):
    '''给用户发送验证码'''
    phonenum = request.GET.get('phonenum')
    print("电话：", phonenum)
    if send_vcode(phonenum):
        return JsonResponse({'code': 0, 'data': None})
    else:
        return JsonResponse({'code': 1000, 'data': '验证码发送失败'})


def submit_vcode(request):
    '''提交验证码，执行登录注册'''
    phonenum = request.POST.get('phonenum')
    vcode = request.POST.get('vcode')

    key = 'Vcode-%s' % phonenum
    cached_vcode = cache.get(key)

    if vcode and vcode == cached_vcode:
        try:
            user = User.objects.get(phonenum=phonenum)  # 从数据库获取用户
        except User.DoesNotExist:
            # 如果用户不存在，则执行注册流程
            user = User.objects.create(phonenum=phonenum, nickname=phonenum)

        # 在 Session 中记录用户登录的状态
        request.session['uid'] = user.id

        return JsonResponse({'code': 0, 'data': user.to_dict()})
    else:
        return JsonResponse({'code': 1001, 'data': '验证码错误'})


def show_profile(request):
    '''查看个人资料'''
    uid = request.session.get('uid')
    profilem, _ = Profile.objects.get_or_create(id=uid)
    data = profilem.to_dict()
    return JsonResponse({'code': 0, 'data': data})


def update_profile(request):
    '''更新个人资料'''

    userform = UserForm(request.POST)
    profileform = ProfileForm(request.POST)
    if userform.is_valid() and profileform.is_valid():
        uid = request.session.get('uid')
        User.objects.filter(id=uid).update(**userform.cleaned_data)
        Profile.objects.get_or_create(id=uid, defaults=profileform.cleaned_data)
        return JsonResponse({'code': 0})
    error = {}
    error.update(userform.errors)
    error.update(profileform.errors)
    return JsonResponse({'code': 1003, 'data': error})


def qn_token(request):
    '''获取七牛云 Token'''
    uid = request.session['uid']
    filename = f'Avatar-{uid}'
    token = gen_token(uid, filename)
    return JsonResponse({
        'code': 0,
        'data': {
            'token': token,
            'key': filename,
        }
    })



def qn_callback(request):
    '''七牛云回调接口'''
    uid = request.POST.get('uid')
    key = request.POST.get('key')
    avatar_url = get_res_url(key)
    User.objects.filter(id=uid).update(avatar=avatar_url)
    return JsonResponse({'code': 0, 'data': avatar_url})

