from django.http import JsonResponse
from django.core.cache import cache
from libs.http import render_json
from user.logics import send_vcode
from user.models import User
from user.models import Profile
from user.forms import UserForm
from user.forms import ProfileForm
from libs.qn_cloud import get_token
from libs.qn_cloud import get_res_url
from common import errors
from common import keys


def fetch_vcode(request):
    '''给用户发送验证码'''
    phonenum = request.GET.get('phonenum')
    print("电话：",phonenum)
    if send_vcode(phonenum):
        return render_json()
    else:
        return JsonResponse(data='验证码发送失败',code=1000)


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

        return JsonResponse(data=user.to_dict())
    else:
        return JsonResponse(data='验证码错误',code = 1001)


def show_profile(request):
    '''查看个人资料'''
    uid = request.session['uid']
    profile,_ = User.objects.get_or_create(id=uid)
    return JsonResponse(data=profile.to_dict())


def update_profile(request):
    '''更新个人资料'''

    # 定义form对象
    user_form = UserForm(request.POST)
    profile_form = ProfileForm(request.POST)

    # 检查验证对象
    if user_form.is_valid() and profile_form.is_valid():
        uid = request.session['uid']
        user = User.objects.get(id=uid)
        User.objects.filter(id=uid).update(**user_form.cleaned_data)
        Profile.objects.update_or_create(id = uid,defaults=profile_form.cleaned_data)

        return JsonResponse()
    else:
        err = {}
        err.update(user_form.errors)
        err.update(profile_form.errors)
        return JsonResponse(data=err,code=1003)


def qn_token(request):
    '''获取七牛云 Token'''
    uid = request.session['uid']
    filename = f'Avatar-{uid}'
    token = get_token(uid,filename)
    return JsonResponse({
        'code':0,
        'data':{
            'token':token,
            'key':filename
        }
    })


def qn_callback(request):
    '''七牛云回调接口'''
    uid = request.POST.get('uid')
    key = request.POST.get('key')
    avatar_url = get_res_url(key)
    User.objects.filter(id=uid).update(avatar = avatar_url)
    return JsonResponse(data=avatar_url)





