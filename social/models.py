from django.db import models, IntegrityError

# Create your models here.
from django.db.models import Q

from common import errors


class Swiped(models.Model):
    """滑动记录表"""
    STYPES = (
        ('like', '喜欢'),
        ('superlike', '超级喜欢'),
        ('dislike', '不喜欢')
    )
    uid = models.IntegerField(verbose_name='滑动者的ID')
    sid = models.IntegerField(verbose_name='被滑动者ID')
    stype = models.CharField(max_length=12, choices=STYPES, verbose_name='滑动类型')
    stime = models.DateTimeField(auto_now_add=True, verbose_name='滑动时间')

    class Meta:
        unique_together = ['uid', 'sid']

    @classmethod
    def swipe(cls, uid, sid, stype):
        try:
            # 给自己创建超级喜欢用户
            cls.objects.create(uid=uid, sid=sid, stype=stype)
        except IntegrityError:
            raise errors.RepeatSwipeErr

    @classmethod
    def is_like(cls, uid, sid):
        """检查是否喜欢过某人"""
        swiped = cls.objects.filter(uid=uid, sid=sid).first()

        if not swiped:
            return None
        elif swiped.stype in ['like', 'superlike']:
            return True
        else:
            return False


class Friend(models.Model):
    uid1 = models.IntegerField(verbose_name='UID_1')
    uid2 = models.IntegerField(verbose_name='UID_2')

    class Meta:
        unique_together = ['uid1', 'uid2']

    @classmethod
    def make_friends(cls, uid1, uid2):
        uid1, uid2 = (uid1, uid2) if uid1 < uid2 else (uid2, uid1)
        return cls.objects.create(uid1=uid1, uid2=uid2)

    @classmethod
    def breakoff(cls, uid1, uid2):
        """删除好友关系"""
        uid1, uid2 = (uid2, uid1) if uid1 > uid2 else (uid1, uid2)
        cls.objects.filter(uid1=uid1, uid2=uid2).delete()

    @classmethod
    def friend_ids(cls, uid):
        """查找自己的所有好友ID"""
        uid_list = []
        friends = cls.objects.filter(Q(uid1=uid) | Q(uid2=uid))
        for friend in friends:
            if friend.uid1 == uid:
                uid_list.append(friend.uid2)
            else:
                uid_list.append(friend.uid1)
        return uid_list
