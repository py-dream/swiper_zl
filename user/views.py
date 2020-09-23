import random

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from django.core.cache import cache

# Create your views here.
from django.views import View

from user.models import User
from tools.send_sms import send_sms

# 发送短信
def phone_sms(request):
    if request.method == "POST":
        phonenum = request.POST.get("phonenum")
        print('phone:',phonenum)

        code = random.randint(1000,9999)
        code = str(code)
        ret = send_sms(phonenum,code)
        if ret == 'success':
            cache.set(phonenum, code, 60 * 30)
            return HttpResponse("短信发送成功，请查收！")
        elif ret == 'error':
            cache.set(phonenum, '0000', 60 * 30)
            return HttpResponse("短信发送成功，请查收！")

        return HttpResponse("短信发送失败！")

    return HttpResponse("请求方式错误！")

# 验证短信
def verification(request):
    if request.method == "POST":
        # 手机号，验证码获取
        phonenum = request.POST.get('phonenum')
        code = request.POST.get('code')

        # 验证
        correct_code = cache.get(phonenum)
        print('correct_code:', correct_code)

        # 数据库验证
        user = User.objects.filter(phonenum=phonenum).first()
        if not user:
            if code == correct_code:
                obj = User()
                obj.phonenum = phonenum
                obj.nickname = phonenum
                obj.save()
                request.session['uid'] = obj.id
                return HttpResponse('登陆注册成功！')
        else:
            if code == correct_code:
                request.session['uid'] = user.id
                return HttpResponse('登陆成功！')

    return HttpResponse("请求方式错误！")

class user_info(View):

    def get(self,request):
        phonenum = request.GET.get("phonenum")
        user = User.objects.get(phonenum=phonenum)
        if user:
            data = {
                'id':user.id,
                'phonenum':user.phonenum,
                'gender':user.gender,
                'nickname':user.nickname,
                'birthday':user.birthday,
                'location':user.location,
                'avatar':user.avatar
            }
            return JsonResponse(data)
        return HttpResponse("没有次用户")

    def post(self,request):
        phonenum = request.POST.get("phonenum")
        nickname = request.POST.get("nickname")
        gender = request.POST.get('gender')
        birthday = request.POST.get("birthday")
        avatar = request.POST.get("avatar")
        location = request.POST.get("location")
        user = User.objects.get(phonenum=phonenum)
        if user:
            if nickname:
                user.nickname = nickname
            if gender:
                user.gender = gender
            if birthday:
                user.birthday = birthday
            if avatar:
                user.avatar = avatar
            if location:
                user.location = location
            user.save()
            return HttpResponse("修改成功！")
        else:
            return HttpResponse("修改失败！")









