from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import WoodModel
from .forms import WoodForm
from order.models import FORM_TYPE, WoodFormModel
from django.views.generic import ListView


def add(request):
    if request.method == 'POST':
        form = WoodForm(request.POST)
        if form.is_valid() and form.save():
            return HttpResponseRedirect('/home/wood/list/')
    else:
        form = WoodForm()
    return render(request, 'wood.html', {'form': form})


def submit(request):
    name = request.POST.get('name')
    surface = request.POST.get('surface')
    note = request.POST.get('note')
    factory = request.POST.get('factory')
    dic = {"name": name, "surface": surface, "note": note, "factory": factory}
    WoodModel.objects.create(**dic)
    return HttpResponseRedirect('/home/wood/list/')


def enable(request):
    obj_id = request.GET.get('id')
    obj = WoodModel.objects.get(id=obj_id)
    obj.enable = not obj.enable
    obj.save()
    return HttpResponseRedirect('/home/wood/list/')


def delete(request):
    obj_id = request.GET.get('id')
    try:
        WoodModel.objects.filter(id=obj_id).delete()
    except Exception as e:
        messages.success(request, e.args)
    return HttpResponseRedirect('/home/wood/list/')


class WoodListView(ListView):
    paginate_by = 15
    model = WoodModel
    template_name = 'woodlist.html'
    context_object_name = 'object_list'

    def get_queryset(self):  # 重写get_queryset方法
        # 获取所有is_deleted为False的用户，并且以时间倒序返回数据
        return WoodModel.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super(WoodListView, self).get_context_data(**kwargs)
        return context


def form_add(request):
    q = Q(enable=True)
    obj_id = request.GET.get('id')
    if obj_id:
        q.add(Q(id=obj_id), Q.AND)
    woods = WoodModel.objects.filter(q).order_by('name')
    types = FORM_TYPE
    return render(request, 'woodform.html', context={'woods': woods, "types": types})


def form_submit(request):
    time = request.POST.get('time')
    wood_id = request.POST.get('name')
    count = int(request.POST.get('count'))
    form_type = int(request.POST.get('type'))
    note = request.POST.get('note')
    wood = WoodModel.objects.get(id=wood_id)
    dic = {"arrive_date": time, "name": wood, "count": count, "type": form_type, "note": note, "sure": True}
    success = WoodFormModel.objects.create(**dic)
    if success:
        sync_count(wood_id, count, form_type == 1)
    return HttpResponseRedirect('/home/wood/form/list/')


def form_sure(request):
    obj_id = request.GET.get('id')
    obj = WoodFormModel.objects.get(id=obj_id)
    obj.sure = not obj.sure
    if obj.sure:
        if obj.type == '1':
            obj.name.count += obj.count
        else:
            obj.name.count -= obj.count
    else:
        if obj.type == '1':
            obj.name.count -= obj.count
        else:
            obj.name.count += obj.count
    obj.name.save()
    obj.save()
    return HttpResponseRedirect('/home/wood/form/list/')


def form_complete(request):
    obj_id = request.GET.get('id')
    obj = WoodFormModel.objects.get(id=obj_id)
    obj.complete = not obj.complete
    obj.save()
    return HttpResponseRedirect('/home/wood/form/list/')


def form_delete(request):
    obj_id = request.GET.get('id')
    form = WoodFormModel.objects.get(id=obj_id)
    if form.sure:
        messages.success(request, "请先取消确认")
    else:
        try:
            WoodFormModel.objects.filter(id=obj_id).delete()
        except Exception as e:
            messages.success(request, e.args)
    return HttpResponseRedirect('/home/wood/form/list/')


class WoodFormListView(ListView):
    paginate_by = 15
    model = WoodFormModel
    template_name = 'woodformlist.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        name = self.request.GET.get('name')
        obj_id = self.request.GET.get('id')
        q = Q()
        if name:
            id_list = WoodModel.objects.filter(name__contains=name)
            q.add(Q(name_id__in=id_list), Q.OR)
        if obj_id:
            q.add(Q(name_id=obj_id), Q.AND)
        return WoodFormModel.objects.filter(q).order_by('-id')

    def get_context_data(self, **kwargs):
        context = super(WoodFormListView, self).get_context_data(**kwargs)
        return context


def sync_count(mid, count, state):
    obj = WoodModel.objects.get(id=mid)
    if state:
        WoodModel.objects.filter(id=mid).update(count=(obj.count + count))
    else:
        WoodModel.objects.filter(id=mid).update(count=(obj.count - count))
