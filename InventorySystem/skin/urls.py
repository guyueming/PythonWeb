from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add, name='skin_add'),
    path('list/', views.SkinListView.as_view(), name='skin_list'),
    path('submit/', views.submit),
    path('enable/', views.enable),

    path('form/add', views.form_add, name='skin_form_add'),
    path('form/list/', views.SkinFormListView.as_view(), name='skin_form_list'),
    path('form/submit/', views.form_submit),
    path('form/complete/', views.form_complete),
]
