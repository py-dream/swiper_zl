import datetime

from django.db import models
from django.db.models import query

from libs.cache import rds


def get(self, *args, **kwargs):
    """
        Perform the query and return a single object matching the given
        keyword arguments.
    """
    cls_name = self.model.__name__
    # 先从缓存里面取数据
    pk = kwargs.get('pk') or kwargs.get('id')
    if pk is not None:
        key = 'Model-%s-%s' % (cls_name, pk)
        model_obj = rds.get(key, pk)
        # print('缓存')
        if isinstance(model_obj, self.model):
            return model_obj

    # 从数据库里面取
    model_obj = self._get(*args, **kwargs)
    # print("数据库")
    # 将数据写入缓存
    key = 'Model-%s-%s' % (cls_name, model_obj.pk)
    rds.set(key, model_obj)
    return model_obj


def save(self, force_insert=False, force_update=False, using=None,
         update_fields=None):
    """
        Save the current instance. Override this in a subclass if you want to
        control the saving process.

        The 'force_insert' and 'force_update' parameters can be used to insist
        that the "save" must be an SQL insert or update (or equivalent for
        non-SQL backends), respectively. Normally, they should not be set.
        """
    # 调用原始方法将数据保存到数据库里面
    self._save(force_insert=False, force_update=False, using=None,
               update_fields=None)

    # 将对象保存到缓存里面
    key = 'Model-%s-%s' % (self.__class__.__name__, self.pk)
    rds.set(key, self)


def to_dict(self, exclude=()):
    """将用户转换成字典"""

    attr_dict = {}

    # 找到对象身上所有字段名称
    for fielsd in self._meta.fields:
        if fielsd.attname in exclude:
            continue

        # 找到字段名对应的值
        value = getattr(self, fielsd.attname)

        # 将data和datatime类型的值转成字符串类型，防止json序列化报错
        if isinstance(value, (datetime.datetime, datetime.date)):
            value = str(value)

        attr_dict[fielsd.attname] = value

    return attr_dict


def path_orm():
    query.QuerySet._get = query.QuerySet.get
    query.QuerySet.get = get

    models.Model._save = models.Model.save
    models.Model.save = save

    models.Model.to_dict = to_dict
