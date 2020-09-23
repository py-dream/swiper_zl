from django.db import models

# Create your models here.

class User(models.Model):
    phonenum = models.CharField(max_length=11,null=False)
    nickname = models.CharField(max_length=32)
    gender = models.CharField(max_length=6, choices=(('boy', '男'), ('girl', '女')),default='boy')
    birthday = models.DateField(default='2010-01-01')
    avatar = models.CharField(max_length=256)
    location = models.CharField(max_length=256)

    class Meta:
        db_table = 'user'



