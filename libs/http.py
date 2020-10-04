import json

from django.conf import settings
from django.http import HttpResponse


def render_json(data=None, code=0):
    result = {
        'data': data,
        'code': code
    }
    if settings.DEBUG == True:
        json_str = json.dumps(result,ensure_ascii=False,indent=4,sort_keys=True)
    else:
        json_str = json.dumps(result,ensure_ascii=False,separators=(',',':'))
    return HttpResponse(content=json_str,content_type='application/json')