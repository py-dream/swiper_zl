from libs.http import render_json
from social import logics
from social.logics import superlike_someone, like_someone, dislike_someone, rewind_last_swiper, find_my_fans
from social.models import Friend
from user.models import User
from vip.logics import perm_required


def rcmd_users(request):
    """获取推荐用户"""
    users = logics.rcmd(request.uid)
    users_dats = [user.to_dict() for user in users]
    return render_json(users_dats)


@perm_required('superlike')
def superlike(request):
    """超级喜欢（上滑）"""
    sid = int(request.POST.get('sid'))
    matched = superlike_someone(request.uid, sid)
    return render_json({'is_matched': matched})


def like(request):
    """喜欢（右滑）"""
    sid = int(request.POST.get('sid'))
    matched = like_someone(request.uid, sid)
    return render_json({'is_matched': matched})


def dislike(request, sid):
    """不喜欢（左滑）"""
    dislike_someone(request.uid, sid)
    return render_json()


@perm_required('rewind')
def rewind(request):
    """反悔"""
    rewind_last_swiper(request.uid)
    return render_json()


@perm_required('show_fans')
def show_fans(request):
    """查看喜欢我的的人"""
    fans = find_my_fans(request.uid)
    user_data = [fan.to_dict() for fan in fans]

    return render_json(user_data)


def show_friends(request):
    """查看好友"""
    friends_list = Friend.friend_ids(request.uid)
    friends = User.objects.filter(id__in=friends_list)
    user_data = [friend.to_dict() for friend in friends]
    return render_json(user_data)
