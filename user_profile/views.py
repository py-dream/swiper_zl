from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from requests import Response


def show(request):
    phone = phone
    profile = profile.object.filter(phonenum = phonenum).first()
    if profile:
        profiledata = {
            'code':0,
            'data':{
                'id':profile.id,
                'dating_gender':profile.dating_gender,
                'dating_location':profile.dating_location,
                'max_distance':profile.max_distance,
                'min_distance':profile.min_distance,
                'max_dating_age':profile.max_dating_age,
                'min_dating_age':profile.min_dating_age,
                'vibration':profile.vibration,
                'only_matched':profile.only_matched,
                'auto_play':profile.auto_play
            }
        }
    return HttpResponse(josn.dumps(profiledata))


def update(request):
    phone = phone
    profile = profile.object.filter(phonenum = phonenum).first()
    nickname = request.POST.get('nickname')
    birthday = request.POST.get('birthday')
    gender = request.POST.get('gender')
    location = request.POST.get('location')
    dating_gender = request.POST.get('dating_gender')
    dating_location = request.POST.get('dating_location')
    max_distance = request.POST.get('max_distance')
    min_distance = request.POST.get('min_distance')
    max_dating_age = request.POST.get('max_dating_age')
    min_dating_age = request.POST.get('min_dating_age')
    vibration = request.POST.get('vibration')
    only_matched = request.POST.get('only_matched')
    auto_play = request.POST.get('auto_play')

    profile.nickname = nickname
    profile.irthday = birthday
    profile.ender = gender
    profile.location = location
    profile.dating_gender = dating_gender
    profile.dating_location = dating_location
    profile.max_distance = max_distance
    profile.min_distance = min_distance
    profile.max_dating_age = max_dating_age
    profile.min_dating_age = min_dating_age
    profile.vibration = vibration
    profile.only_matched = only_matched
    profile.auto_play = auto_play
    profile.save()
    return None