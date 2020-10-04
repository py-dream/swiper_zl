from common import errors
from user.models import User
import logging

err_log = logging.getLogger('err')


def perm_required(perm_name):
    """检查当前用户购买的VIP是否具有某权限"""

    def deco(view_func):
        def wrapper(request, *args, **kwargs):
            user = User.objects.get(id=request.uid)
            # 权限验证
            if user.vip.has_perm(perm_name):
                return view_func(request, *args, **kwargs)
            else:
                err_log.error('没有这个权限')
                raise errors.PermissionErr

        return wrapper

    return deco
