from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import SalesmanModel
from django.views.generic import ListView


def add(request):
    return render(request, 'salesman.html')


def submit(request):
    name = request.POST.get('name')
    phone = request.POST.get('phone')
    note = request.POST.get('note')
    dic = {"name": name, "phone": phone, "note": note}
    SalesmanModel.objects.create(**dic)
    return HttpResponseRedirect('/home/salesman/list/')


def enable(request):
    return render(request, 'salesmanlist.html')


def delete(request):
    return render(request, 'salesmanlist.html')


class SalesmanListView(ListView):
    paginate_by = 15
    model = SalesmanModel
    template_name = 'salesmanlist.html'
    context_object_name = 'object_list'

    def get_queryset(self):  # 重写get_queryset方法
        return SalesmanModel.objects.all().order_by('-id')

    def get_context_data(self, **kwargs):
        context = super(SalesmanListView, self).get_context_data(**kwargs)
        # context['xxx'] = 'xxx' #添加额外的键值对，传到模板中
        return context
