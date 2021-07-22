
from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_orders, name='order_adds'),
    path('add/<int:pk>/', views.add_order, name='order_add'),
    path('list/', views.OrderListView.as_view(), name='order_list'),
    path('sure/', views.make_sure),
    path('del/', views.make_delete),

    path('head/list/', views.OrderHeadListView.as_view(), name='order_list'),
    path('head/sure/', views.make_head_sure),
    path('head/complete/', views.make_head_complete),
    path('head/del/', views.make_head_delete),
    path('head/view/<int:pk>/', views.view_orders, name='view_orders'),
    path('head/view/detail/<int:pk>/', views.view_detail_orders, name='view_detail_orders'),
    path('head/edit/<int:pk>/', views.edit_orders, name='edit_orders'),
]
