from django.http import HttpResponse, JsonResponse
from django.utils.deprecation import MiddlewareMixin


class AutherMiddleware(MiddlewareMixin):
    white_list = ['/user/phone_sms/', '/user/verification/']

    def process_request(self, request):

        if request.path in self.white_list:
            return

        uid = request.session.get('uid')
        if not uid:
            return JsonResponse({'code': 1002, 'data': '用户未登录'})
