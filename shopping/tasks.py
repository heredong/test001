# -*- coding: utf-8 -*-
from celery import task
import time

from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.template.loader import get_template


@task
def send_my_mail(title,message,email):
    print('tasks中开始发送')
    email_from = settings.DEFAULT_FROM_EMAIL

    recivies =email
    print('receives是')
    print(recivies)
    url = message

    template = get_template('temp.html')

    html_str = template.render({'url':url})

    print(html_str)

    send_mail(
        title,message,email_from,recivies
    )
    print('tasks中发送成功')
    return HttpResponse('ok')