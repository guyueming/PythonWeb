from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add, name='add_wood'),
    path('list/', views.WoodListView.as_view(), name='wood_list'),
    path('submit/', views.submit),
    path('enable/', views.enable),
    path('del/', views.delete),

    path('form/add', views.form_add, name='add_form'),
    path('form/list/', views.WoodFormListView.as_view(), name='wood_form_list'),
    path('form/submit/', views.form_submit),
    path('form/sure/', views.form_sure),
    path('form/complete/', views.form_complete),
    path('form/del/', views.form_delete),
]
