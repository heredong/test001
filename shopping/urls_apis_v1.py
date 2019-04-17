from django.conf.urls import url
from .apis import *
urlpatterns =[
    url(r"^register$",RegisterAPI.as_view(),name='register'),
    url(r"^login$",LoginAPI.as_view(),name='login'),
    url(r"^cart_item$",ItemCartAPI.as_view(),name='cart_item'),
    url(r"^cart/status$",CartItemStatusAPI.as_view(),name='cart/status'),
    url(r"^cart-status$",cart_data_status_api,name='cart-status'),
    url(r"^cart/options$",CartDataOptionAPI.as_view(),name='cart/options'),
    url(r"^orderitem/(?P<pk>\d+)",OrderItemAPI.as_view(),name='orderitem'),
]