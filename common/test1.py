import sys

# from common.test import add
# from libs.cache import rds

import os
import django
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'swiper_zl.settings')

django.setup()

from user.models import User
if __name__ == '__main__':
    # a = add.delay(5,5)
    # print(a)
    print(sys.path)
    # rds.set("a","aa",60)
    user = User.objects.get(id=2)
    print(user)
