from django.db import models


class Vip(models.Model):
    """会员表"""
    name = models.CharField(max_length=32, unique=True, verbose_name="会员名称")
    level = models.IntegerField(verbose_name="会员等级")
    duration = models.IntegerField(verbose_name="会员时长")
    price = models.FloatField(verbose_name="会员价格")

    def has_perm(self,perm_name):
        perm = Permission.objects.get(name=perm_name)
        return VipPermRelation.objects.filter(vip_level=self.level,perm_id=perm.id)


class Permission(models.Model):
    """权限表"""
    name = models.CharField(max_length=32, unique=True, verbose_name="权限名")
    description = models.TextField(verbose_name="权限描述")


class VipPermRelation(models.Model):
    vip_level = models.IntegerField(verbose_name="会员等级")
    perm_id = models.IntegerField(verbose_name="权限ID")

