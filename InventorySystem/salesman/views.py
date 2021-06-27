from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import SalesmanModel
from .forms import SalesmanForm
from django.views.generic import ListView
from django.contrib import messages


def add(request):
    if request.method == 'POST':
        form = SalesmanForm(request.POST)
        if form.is_valid():
            dic = {"name": form.cleaned_data['name'], "note": form.cleaned_data['note'], "phone": form.cleaned_data['phone']}
            SalesmanModel.objects.create(**dic)
            return HttpResponseRedirect('/home/salesman/list/')
    else:
        form = SalesmanForm()
    return render(request, 'salesman.html', {'form': form})


def submit(request):
    name = request.POST.get('name')
    phone = request.POST.get('phone')
    note = request.POST.get('note')
    dic = {"name": name, "phone": phone, "note": note}
    SalesmanModel.objects.create(**dic)
    return HttpResponseRedirect('/home/salesman/list/')


def enable(request):
    obj_id = request.GET.get('id')
    obj = SalesmanModel.objects.get(id=obj_id)
    obj.enable = not obj.enable
    obj.save()
    return HttpResponseRedirect('/home/salesman/list/')


def delete(request):
    obj_id = request.GET.get('id')
    try:
        SalesmanModel.objects.filter(id=obj_id).delete()
    except Exception as e:
        messages.success(request, e.args)
    return HttpResponseRedirect('/home/salesman/list/')


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
