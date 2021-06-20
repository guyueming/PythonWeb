from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import PaperModel
from order.models import FORM_TYPE, PaperFormModel
from django.views.generic import ListView


def add(request):
    return render(request, 'paper.html')


def submit(request):
    name = request.POST.get('name')
    model = request.POST.get('model')
    factory = request.POST.get('factory')
    color = request.POST.get('color')
    note = request.POST.get('note')
    dic = {"name": name, "type": model, "factory": factory, "note": note, "color": color}
    PaperModel.objects.create(**dic)
    return HttpResponseRedirect('/home/paper/list/')


def enable(request):
    obj_id = request.GET.get('id')
    obj = PaperModel.objects.get(id=obj_id)
    obj.enable = not obj.enable
    obj.save()
    return HttpResponseRedirect('/home/paper/list/')


def delete(request):
    obj_id = request.GET.get('id')
    try:
        PaperModel.objects.filter(id=obj_id).delete()
    except Exception as e:
        messages.success(request, e.args)
    return HttpResponseRedirect('/home/paper/list/')


class PaperListView(ListView):
    paginate_by = 15
    model = PaperModel
    template_name = 'paperlist.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        return PaperModel.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super(PaperListView, self).get_context_data(**kwargs)
        # context['xxx'] = 'xxx' #添加额外的键值对，传到模板中
        return context


def form_add(request):
    object_list = PaperModel.objects.filter(enable=True).order_by('name')
    types = FORM_TYPE
    return render(request, 'paperform.html', context={'object_list': object_list, "types": types})


def form_submit(request):
    time = request.POST.get('time')
    mid = request.POST.get('name')
    count = int(request.POST.get('count'))
    form_type = int(request.POST.get('type'))
    obj = PaperModel.objects.get(id=mid)
    dic = {"arrive_date": time, "name": obj, "count": count, "type": form_type, "sure": True}
    PaperFormModel.objects.create(**dic)
    sync_count(mid, count, form_type == 1)
    return HttpResponseRedirect('/home/paper/form/list/')


def form_sure(request):
    obj_id = request.GET.get('id')
    obj = PaperFormModel.objects.get(id=obj_id)
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
    return HttpResponseRedirect('/home/paper/form/list/')


def form_complete(request):
    obj_id = request.GET.get('id')
    obj = PaperFormModel.objects.get(id=obj_id)
    obj.complete = not obj.complete
    obj.save()
    return HttpResponseRedirect('/home/paper/form/list/')


def form_delete(request):
    obj_id = request.GET.get('id')
    form = PaperFormModel.objects.get(id=obj_id)
    if form.sure:
        messages.success(request, "请先取消确认")
    else:
        try:
            PaperFormModel.objects.filter(id=obj_id).delete()
        except Exception as e:
            messages.success(request, e.args)
    return HttpResponseRedirect('/home/paper/form/list/')


class PaperFormListView(ListView):
    paginate_by = 15
    model = PaperFormModel
    template_name = 'paperformlist.html'
    context_object_name = 'object_list'

    def get_queryset(self):  # 重写get_queryset方法
        return PaperFormModel.objects.all().order_by('-id')

    def get_context_data(self, **kwargs):
        context = super(PaperFormListView, self).get_context_data(**kwargs)
        # context['xxx'] = 'xxx' #添加额外的键值对，传到模板中
        return context


def sync_count(mid, count, state):
    obj = PaperModel.objects.get(id=mid)
    if state:
        PaperModel.objects.filter(id=mid).update(count=(obj.count + count))
    else:
        PaperModel.objects.filter(id=mid).update(count=(obj.count - count))

