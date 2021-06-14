from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import SkinModel
from order.models import FORM_TYPE, SkinFormModel
from django.views.generic import ListView


def add(request):
    return render(request, 'skin.html')


def submit(request):
    name = request.POST.get('name')
    note = request.POST.get('note')
    dic = {"name": name, "note": note}
    SkinModel.objects.create(**dic)
    return HttpResponseRedirect('/home/skin/list/')


def enable(request):
    return render(request, 'skinlist.html')


def delete(request):
    return render(request, 'skinlist.html')


class SkinListView(ListView):
    paginate_by = 15
    model = SkinModel
    template_name = 'skinlist.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        return SkinModel.objects.filter(enable=True).order_by('-last_mod_time')

    def get_context_data(self, **kwargs):
        context = super(SkinListView, self).get_context_data(**kwargs)
        # context['xxx'] = 'xxx' #添加额外的键值对，传到模板中
        return context


def form_add(request):
    object_list = SkinModel.objects.filter(enable=True).order_by('name')
    return render(request, 'skinform.html', context={'object_list': object_list, "types": FORM_TYPE})


def form_submit(request):
    time = request.POST.get('time')
    mid = request.POST.get('name')
    count = int(request.POST.get('count'))
    form_type = int(request.POST.get('type'))
    sure = request.POST.get('complete')
    obj = SkinModel.objects.get(id=mid)
    note = request.POST.get('note')
    dic = {"arrive_date": time, "name": obj, "count": count, "type": form_type, "note": note}
    if sure:
        dic["sure"] = sure
        sync_count(mid, count, form_type == 1)
    SkinFormModel.objects.create(**dic)
    return HttpResponseRedirect('/home/skin/form/list/')


def form_sure(request):
    return render(request, 'skinformlist.html')


def form_complete(request):
    return render(request, 'skinformlist.html')


def form_delete(request):
    return render(request, 'skinformlist.html')


class SkinFormListView(ListView):
    paginate_by = 15
    model = SkinFormModel
    template_name = 'skinformlist.html'
    context_object_name = 'object_list'

    def get_queryset(self):  # 重写get_queryset方法
        # 获取所有is_deleted为False的用户，并且以时间倒序返回数据
        return SkinFormModel.objects.all().order_by('-last_mod_time')

    def get_context_data(self, **kwargs):
        context = super(SkinFormListView, self).get_context_data(**kwargs)
        # context['xxx'] = 'xxx' #添加额外的键值对，传到模板中
        return context


def sync_count(mid, count, state):
    obj = SkinModel.objects.get(id=mid)
    if state:
        SkinModel.objects.filter(id=mid).update(count=(obj.count + count))
    else:
        SkinModel.objects.filter(id=mid).update(count=(obj.count - count))