from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add, name='paper_add'),
    path('list/', views.PaperListView.as_view(), name='paper_list'),
    path('submit/', views.submit),
    path('enable/', views.enable),
    path('del/', views.delete),
    path('output/', views.output),

    path('form/add', views.form_add, name='add_form'),
    path('form/list/', views.PaperFormListView.as_view(), name='paper_form_list'),
    path('form/submit/', views.form_submit),
    path('form/sure/', views.form_sure),
    path('form/complete/', views.form_complete),
    path('form/del/', views.form_delete),
]
