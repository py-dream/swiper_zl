import datetime

from django.db.transaction import atomic

from common import keys, errors
from common.keys import REWIND_TIMES_K
from libs.cache import rds
from social.models import Swiped, Friend
from swiper_zl.config import REWIND_TIMEOUT, REWIND_TIMES
from user.models import Profile, User


def rcmd_from_queue(uid):
    """从优先推荐队列进行推荐"""
    uid_list = rds.lrange(keys.FIRST_RCMD_Q % uid, 0, 19)
    uid_list = [int(uid) for uid in uid_list]
    return User.objects.filter(id__in=uid_list)


def rcmd_from_db(uid, num=20):
    """正常系统推荐"""

    profile = Profile.objects.get(id=uid)

    # 计算出生日期范围
    today = datetime.date.today()
    earliest_birth = today - datetime.timedelta(profile.max_dating_age * 365)
    latest_birth = today - datetime.timedelta(profile.min_dating_age * 365)

    # 获取
    sid_list = Swiped.objects.filter(uid=uid).values_list('sid', flat=True)

    users = User.objects.filter(
        location=profile.dating_location,
        gender=profile.dating_gender,
        birthday__range=[earliest_birth, latest_birth]
    ).exclude(id__in=sid_list)[:num]

    return users


def rcmd(uid):
    """推荐滑动用户"""

    # 超级喜欢推荐
    first_users = rcmd_from_queue(uid)
    remain = 20 - len(first_users)
    if remain:
        second_users = rcmd_from_db(uid, remain)
        return set(first_users) | set(second_users)
    else:
        return first_users


@atomic
def superlike_someone(uid, sid):
    """超级喜欢"""
    # 添加超级喜欢记录
    Swiped.swipe(uid, sid, 'superlike')

    # 删除优先推进列表
    rds.lrem(keys.FIRST_RCMD_Q % uid, count=0, value=sid)

    # 检查对方是否喜欢自己
    liked = Swiped.is_like(sid, uid)

    if liked is True:
        Friend.make_friends(uid, sid)
        return True
    elif liked is False:
        return False
    else:
        rds.rpush(keys.FIRST_RCMD_Q % sid, uid)
        return False


@atomic
def like_someone(uid, sid):
    # 滑动记录添加
    Swiped.swipe(uid, sid, 'like')
    # 强制删除优先推荐队列中的sid
    rds.lrem(keys.FIRST_RCMD_Q % uid, count=0, value=sid)
    # 检查对方是否喜欢自己
    liked = Swiped.is_like(sid, uid)
    if liked:
        Friend.make_friends(uid, sid)
        return True
    else:
        return False


def dislike_someone(uid, sid):
    # 滑动记录添加
    Swiped.swipe(uid, sid, 'dialike')

    # 强制删除优选队列sid
    rds.lrem(keys.FIRST_RCMD_Q % uid, 0, sid)


def rewind_last_swiper(uid):
    """反悔上一次滑动，一天只能三次，反悔记录要在五分钟之内"""

    now = datetime.datetime.now()

    # 检查今天是否已经反悔三次
    rewind_key = REWIND_TIMES_K % (now.date(), uid)
    rewind_times = rds.get(rewind_key, 0)
    if rewind_times >= REWIND_TIMES:
        raise errors.RewindLimit

    # 找到最后一次滑动记录
    last_swipe = Swiped.objects.filter(uid=uid).latest('stime')
    print("last_swipe.stime", last_swipe.stime)
    print(type(now), now)
    print(type(last_swipe.stime), last_swipe.stime)
    # 检查最后一次的滑动时间是否在5分钟之内
    # time_past = (now - last_swipe.stime).total_seconds()
    time_past = (now - last_swipe.stime).total_seconds()
    print(time_past)

    if time_past >= REWIND_TIMEOUT:
        raise errors.RewindTimeout
    with atomic():
        if last_swipe.stype in ['like', 'superlike']:
            # 如果成了好友删除好友关系
            Friend.breakoff(uid, last_swipe.sid)

            # 如果上次是超级喜欢，从对方优先队列中删除自己的uid
            if last_swipe.stype == 'superlieke':
                rds.lrem(keys.FIRST_RCMD_Q % last_swipe.sid, 0, uid)

        # 删除最后一次滑动
        last_swipe.delete()

        # 今日反悔次数加1
        rds.set(rewind_key, rewind_times + 1, 86460)


def find_my_fans(uid):
    """查看我的粉丝 （喜欢我还不是朋友）"""
    # 取出我划过的用户
    sid_list = Swiped.objects.filter(uid=uid).values_list('sid', flat=True)

    #  取出所有喜欢我的人
    fans_id_list = Swiped.objects.filter(sid=uid, stype__in=['like', 'superlike']).exclude(
        uid__in=sid_list).values_list('uid', flat=True)

    user = User.objects.filter(id__in=fans_id_list)

    return user
