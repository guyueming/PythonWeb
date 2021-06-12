from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import CustomerModel
from django.views.generic import ListView


def add(request):
    return render(request, 'customer.html')


def submit(request):
    name = request.POST.get('name')
    phone = request.POST.get('phone')
    address = request.POST.get('address')
    note = request.POST.get('note')
    dic = {"name": name, "phone": phone, "address": address, "note": note}
    CustomerModel.objects.create(**dic)
    return HttpResponseRedirect('/home/customer/list/')


def enable(request):
    return render(request, 'customer.html')


class CustomerListView(ListView):
    paginate_by = 15
    model = CustomerModel
    template_name = 'customerlist.html'
    context_object_name = 'object_list'

    def get_queryset(self):  # 重写get_queryset方法
        return CustomerModel.objects.all().order_by('-id')

    def get_context_data(self, **kwargs):
        context = super(CustomerListView, self).get_context_data(**kwargs)
        # context['xxx'] = 'xxx' #添加额外的键值对，传到模板中
        return context
