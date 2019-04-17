import datetime

from django.conf import settings
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from .models import *
from .apis import *
class MyExceptionMiddleWare(MiddlewareMixin):
    def process_exception(self,request,exception):
        if settings.DEBUG == False:
            path = request.path
            print('中间件判断')
            error_msg = str(exception)
            now = datetime.datetime.now()
            msg = "路径{path}出现了{error_msg}".format(
                path=path,
                error_msg=error_msg
            )
            # 去数据库搜索 今天是不是已经发送过邮件了
            if not ErrorLog.objects.filter(
                    api_path=path,
                    msg=msg,
                    date=now.date()
            ).exists():
                print()
                recipient_list = [user[1] for user in settings.ADMINS]
                # 保存错误信息
                ErrorLog.objects.create(api_path=path, msg=msg)
                print('中间件开始发送邮件')
                task_send_mail(title='线上错误',message=msg,email= recipient_list)
                print('中间件发送邮件完成')
            # 发送邮件这个事
        res = {
            "code": 10,
            "msg": str(exception),
            "data": ""
        }

        return JsonResponse(res)