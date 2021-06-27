
from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add, name='order_add'),
    path('adds/', views.add_orders, name='order_adds'),
    path('list/', views.OrderListView.as_view(), name='order_list'),
    path('submit/', views.submit),
    path('sure/', views.make_sure),
    path('complete/', views.make_complete),
    path('del/', views.make_delete),

    path('head/list/', views.OrderHeadListView.as_view(), name='order_list'),
    path('head/submit/', views.submit_order_list),
    path('head/complete/', views.make_head_complete),
    path('head/del/', views.make_head_delete),
]
