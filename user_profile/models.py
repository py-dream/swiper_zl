from django.db import models

# Create your models here.




class Profile(models.Model):
    dating_gender = models.BooleanField(choices=('male','female'))
    dating_location = models.TextField()
    max_distance = models.FloatField()
    min_distance = models.FloatField()
    max_dating_age = models.IntegerField()
    min_dating_age = models.IntegerField()
    vibration = models.NullBooleanField()
    only_matched = models.NullBooleanField()
    auto_play = models.NullBooleanField()
    user = models.ForeignKey(to=User)
