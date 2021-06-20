from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import SkinModel
from order.models import FORM_TYPE, SkinFormModel
from django.views.generic import ListView


def add(request):
    return render(request, 'skin.html')


def submit(request):
    name = request.POST.get('name')
    factory = request.POST.get('factory')
    note = request.POST.get('note')
    dic = {"name": name, "note": note, "factory": factory}
    SkinModel.objects.create(**dic)
    return HttpResponseRedirect('/home/skin/list/')


def enable(request):
    obj_id = request.GET.get('id')
    obj = SkinModel.objects.get(id=obj_id)
    obj.enable = not obj.enable
    obj.save()
    return HttpResponseRedirect('/home/skin/list/')


def delete(request):
    obj_id = request.GET.get('id')
    try:
        SkinModel.objects.filter(id=obj_id).delete()
    except Exception as e:
        messages.success(request, e.args)
    return HttpResponseRedirect('/home/skin/list/')


class SkinListView(ListView):
    paginate_by = 15
    model = SkinModel
    template_name = 'skinlist.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        return SkinModel.objects.all().order_by('name')

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
    obj_id = request.GET.get('id')
    obj = SkinFormModel.objects.get(id=obj_id)
    obj.sure = not obj.sure
    if obj.sure:
        if obj.type == 1:
            obj.name.count += obj.count
        else:
            obj.name.count -= obj.count
    else:
        if obj.type == 1:
            obj.name.count -= obj.count
        else:
            obj.name.count += obj.count
    obj.name.save()
    obj.save()
    return HttpResponseRedirect('/home/skin/form/list/')


def form_complete(request):
    obj_id = request.GET.get('id')
    obj = SkinFormModel.objects.get(id=obj_id)
    obj.complete = not obj.complete
    obj.save()
    return HttpResponseRedirect('/home/skin/form/list/')


def form_delete(request):
    obj_id = request.GET.get('id')
    form = SkinFormModel.objects.get(id=obj_id)
    if form.sure:
        messages.success(request, "请先取消确认")
    else:
        try:
            SkinFormModel.objects.filter(id=obj_id).delete()
        except Exception as e:
            messages.success(request, e.args)
    return HttpResponseRedirect('/home/skin/form/list/')


class SkinFormListView(ListView):
    paginate_by = 15
    model = SkinFormModel
    template_name = 'skinformlist.html'
    context_object_name = 'object_list'

    def get_queryset(self):  # 重写get_queryset方法
        # 获取所有is_deleted为False的用户，并且以时间倒序返回数据
        return SkinFormModel.objects.all().order_by('-id')

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
