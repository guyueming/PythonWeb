from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import CustomerModel
from .forms import CustomerForm
from django.views.generic import ListView
from django.contrib import messages


def add(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            dic = {"name": form.cleaned_data['name'], "note": form.cleaned_data['note'],
                   "address": form.cleaned_data['address'], "phone": form.cleaned_data['phone']}
            CustomerModel.objects.create(**dic)
            return HttpResponseRedirect('/home/customer/list/')
    else:
        form = CustomerForm()
    return render(request, 'customer.html', {'form': form})


def edit(request, pk):
    name = request.POST.get('name')
    phone = request.POST.get('phone')
    address = request.POST.get('address')
    note = request.POST.get('note')
    dic = {"name": name, "phone": phone, "address": address, "note": note}
    CustomerModel.objects.create(**dic)
    return HttpResponseRedirect('/home/customer/list/')


def enable(request):
    obj_id = request.GET.get('id')
    obj = CustomerModel.objects.get(id=obj_id)
    obj.enable = not obj.enable
    obj.save()
    return HttpResponseRedirect('/home/customer/list/')


def delete(request):
    obj_id = request.GET.get('id')
    try:
        CustomerModel.objects.filter(id=obj_id).delete()
    except Exception as e:
        messages.success(request, e.args)
    return HttpResponseRedirect('/home/customer/list/')


class CustomerListView(ListView):
    paginate_by = 15
    model = CustomerModel
    template_name = 'customerlist.html'
    context_object_name = 'object_list'

    def get_queryset(self):  # 重写get_queryset方法
        q = Q()
        name = self.request.GET.get('name')
        if name:
            q.add(Q(name__contains=name), Q.AND)
        return CustomerModel.objects.filter(q).order_by('-id')

    def get_context_data(self, **kwargs):
        context = super(CustomerListView, self).get_context_data(**kwargs)
        # context['xxx'] = 'xxx' #添加额外的键值对，传到模板中
        return context
