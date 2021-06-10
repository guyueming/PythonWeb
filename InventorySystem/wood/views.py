from django.http import HttpResponse
from django.shortcuts import render
from wood.models import WoodModel
from django.views.generic import ListView


def add_wood(request):
    return render(request, 'woodform.html')


class WoodListView(ListView):
    paginate_by = 20
    model = WoodModel
    template_name = 'woodlist.html'
    context_object_name = 'wood_list'

    def get_queryset(self):  # 重写get_queryset方法
        # 获取所有is_deleted为False的用户，并且以时间倒序返回数据
        return WoodModel.objects.filter(is_enable=True).order_by('-created_time')

    def get_context_data(self, **kwargs):
        context = super(WoodListView, self).get_context_data(**kwargs)
        # context['xxx'] = 'xxx' #添加额外的键值对，传到模板中
        return context

    def GET(self, request):
        search_title = request.GET.get('name')
        WoodModel.objects.filter(name=search_title).order_by('-created_time')


def enable(request):
    return render(request, 'woodlist.html')


def submit(request):
    print("注册中....")
    name = request.POST.get('username');
    password = request.POST.get('password');
    print('用户名:', name, ' 密码:', password)
    return HttpResponse('添加成功')
