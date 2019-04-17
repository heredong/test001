# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate, login
from django.core.cache import caches
from django.http import JsonResponse, HttpResponse, QueryDict
from django.urls import reverse
from django.views import View
from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .authentications import LoginAuthentication
from .serializers import *
from .models import Cart, Goods
from .util import get_unique_name, get_sum_money
from .models import MyUser
from .tasks import send_my_mail
user_cache = caches['user']

class LoginAPI(View):
    def post(self,request):
        uname = request.POST.get('uname')
        pwd = request.POST.get('pwd')
        print(uname)
        print(pwd)
        if uname and len(uname)>3:

            user = authenticate(username =uname,password =pwd)
            print(user)
            if user:
                login(request,user)

                res = {
                    'code':0,
                    'msg':'登录成功',
                    'data':reverse('axf:home')
                }
                return JsonResponse(res)
            else:
                res= {
                        'code': 111,
                        'msg': 'not ok',
                        'data': '用户名或密码错误'
                    }
                return JsonResponse(res)
        else:
            res={
                'code':11,
                'msg':'用户名过短',
                'data':'请重新输入'
            }
            return JsonResponse(res)
    def get(self,request):
            # 得到验证码
            message = request.GET.get('verification')
            # print(message)

            uname = request.GET.get('uname')
            # print(uname)
            if get_user(message):
                user001 = MyUser.objects.filter(username=uname).update(
                    is_active=True
                )
                data = {
                    'code':0,
                    'data':'激活成功'
                }
                return JsonResponse(data)
            else:
                data = {
                    'code': 1,
                    'data': 'not ok'
                }
                return JsonResponse(data)

class RegisterAPI(View):
    def post(self,req):
        uname = req.POST.get('username')
        pwd = req.POST.get('pwd')
        confirm_pwd = req.POST.get("confirm_pwd")
        email = req.POST.get('email')
        icon = req.POST.get('icon')
        if uname and len(uname)>=3:
            if pwd and pwd == confirm_pwd:
                if MyUser.objects.filter(username=uname).exists():
                    data = {
                        'code':1,
                        'msg':'用户名已存在'
                    }
                    return JsonResponse(data)
                user = MyUser.objects.create_user(
                    username=uname,
                    password=pwd,
                    is_active = False,
                    email = email,
                    icon =icon
                )

                #发送激活邮件
                print('apis中开始发送邮件')
                title = '验证邮件'
                message = str(get_unique_name())
                message00 = 'http://47.102.107.76:9000/api/shopping/v1/login?verification=' + message + '&&uname=' + str(uname)
                user_cache.set(message, uname, 60 * 60)
                print(email)
                task_send_mail(title=title,message=message00,email=[email])
                print('apis中发送完成')
                data = {
                    'code':0,
                    'data':reverse('axf:login')
                }
                return JsonResponse(data)
            else:
                data = {
                    'code':1,
                    'msg':'两次密码不一致'
                }
                return JsonResponse(data)
        else:
            data = {
                'code':1,
                'msg':'用户名过短0000'
            }
            return JsonResponse(data)

def get_user(message):
    # 去混存尝试拿数据
    res = user_cache.get(message)
    if res:
        print("缓存的")
        return True

class ItemCartAPI(CreateAPIView,UpdateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    authentication_classes =[LoginAuthentication]
    def post(self,request,*args,**kwargs):
        # 允许修改请求参数
        user = request.user
        # 判断用户是否登录
        if not user:
            res = {
                'code':1,
                'msg':'not login',
                'data':reverse('axf:login')
            }
            return Response(res)
        # 为满足序列化器字段需求
        request.data._mutable = True
        request.data['user'] = user.id
        request.data._mutable = False

        goods_id = request.data.get("goods")
        goods = Goods.objects.get(pk=goods_id)
        num = int(request.data.get('num'))

        if num >goods.storenums:
            res = {
                'code':2,
                'msg':'商品库存不足',
                'data':None
            }

            return Response(res)
        cart_items = Cart.objects.filter(
            user=user,
            goods_id=goods_id
        )
        if cart_items.exists():
            cart_item = cart_items.first()
            cart_item.num +=int(num)
            cart_item.save()
            res = {
                'code':0,
                'msg':'ok',
                'data':self.get_serializer(cart_item).data
            }
            return Response(res)
        else:
            serializer = self.get_serializer(data = request.data)

            serializer.is_valid(raise_exception = True)
            self.perform_create(serializer)

            headers = self.get_success_headers(serializer.data)

            res = {
                'code':0,
                'msg':'ok',
                'data':serializer.data
            }
            return Response(res,status=status.HTTP_201_CREATED,headers=headers)

    def put(self, request, *args, **kwargs):
        user = request.user
        # 判断用户是否登录
        if not user:
            res = {
                'code': 1,
                'msg': 'not login',
                'data': reverse('axf:login')
            }
            return Response(res)
        request.data._mutable = True
        num = int(request.data.get("num"))
        if num < 1:
            res = {
                'code':1,
                'msg':'数量不合法',
                'data':''
            }
            return Response(res)
        cart_data = Cart.objects.get(user_id=user.id,goods_id=request.data.get("goods"))
        cart_num = 0
        cart_data.num -= num
        if cart_data.num == 0:
            cart_data.delete()
        else:
            cart_data.save()
            cart_num = cart_data.num
        res={
            'code':0,
            'msg':'ok',
            'data':cart_num
        }
        return Response(res)

def task_send_mail(title,message,email):
    print('views中开始发送邮件')
    print(email)
    send_my_mail.delay(title=title,message=message,email=email)
    print('views中发送成功')
    return HttpResponse('OK')

class CartItemStatusAPI(View):
    def put(self,request):
        params = QueryDict(request.body)
        user = request.user
        cart_id = params.get("cid")
        cart_item = Cart.objects.get(pk=cart_id)
        # 选中状态取反
        cart_item.is_select = not cart_item.is_select
        cart_item.save()

        is_select_all = True
        cart_items = Cart.objects.filter(user=user)
        if cart_items.filter(is_select=False).exists():
            is_select_all=False
        money = get_sum_money(cart_items)

        res = {
            'code':0,
            'msg':'ok',
            'data':{
                'current_item_status':cart_item.is_select,
                'is_select_all':is_select_all,
                'money':"%.2f"%money,
            }
        }
        return JsonResponse(res)

def cart_data_status_api(request):
    user = request.user
    if not user.is_authenticated:
        raise Exception("未登录")
    carts = Cart.objects.filter(user_id=user)
    if not carts.exists():
        raise Exception("未选择商品")
    is_select_all = carts.filter(is_select=False).exists()

    carts.update(is_select=is_select_all)

    sum_money = get_sum_money(carts) if is_select_all else 0
    res = {
        'code':0,
        'msg':'ok',
        'data':{
            'is_select_all':is_select_all,
            'sum_money':sum_money
        }
    }

    return JsonResponse(res)

class CartDataOptionAPI(View):
    def put(self,req):
        params = QueryDict(req.body)
        user = req.user
        if not user.is_authenticated:
            raise Exception('请先登录')
        cart_data = Cart.objects.get(pk=params.get('cid'))
        option = params.get('option')
        if option == 'add':
            cart_data.num += 1
            cart_data.save()
        else:
            cart_data.num -= 1
            if cart_data.num == 0:
                cart_data.delete()
            else:
                cart_data.save()
        cart_items = Cart.objects.filter(user=user)
        sum_money = get_sum_money(Cart.objects.filter(user=user))

        is_select_all = (not cart_items.filter(is_select=False).exists()) and cart_items.exists()
        res = {
            'code':0,
            'msg':'ok',
            'data':{
                'sum_money':sum_money,
                'current_num':cart_data.num,
                'is_select_all':is_select_all,
            }
        }
        return JsonResponse(res)

class OrderItemAPI(DestroyAPIView):
    queryset = OrderItem.objects.filter(order__status=1)
    authentication_classes = [LoginAuthentication]
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        order_id = request.data.get("order_id")
        order_items = self.queryset.filter(order__number=order_id)
        sum_money = 0

        for i in order_items:
            sum_money += (i.goods_num *i.price)

        res = {
            'code':0,
            'mag':'ok',
            'data':{
                'sum_money':sum_money
            }
        }
        return JsonResponse(res)