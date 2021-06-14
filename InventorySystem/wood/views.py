from django.http import HttpResponseRedirect
from django.shortcuts import render
from wood.models import WoodModel
from order.models import FORM_TYPE, WoodFormModel
from django.views.generic import ListView


def add(request):
    return render(request, 'wood.html')


def submit(request):
    name = request.POST.get('name')
    note = request.POST.get('note')
    dic = {"name": name, "note": note}
    WoodModel.objects.create(**dic)
    return HttpResponseRedirect('/home/wood/list/')


def enable(request):
    mid = request.POST.get('id')
    WoodModel.objects.filter(id=mid).update()
    return HttpResponseRedirect('/home/wood/list/')


def delete(request):
    mid = request.POST.get('id')
    WoodModel.objects.filter(id=mid).delete()
    return render(request, 'woodlist.html')


class WoodListView(ListView):
    paginate_by = 15
    model = WoodModel
    template_name = 'woodlist.html'
    context_object_name = 'object_list'

    def get_queryset(self):  # 重写get_queryset方法
        # 获取所有is_deleted为False的用户，并且以时间倒序返回数据
        return WoodModel.objects.filter(enable=True).order_by('-last_mod_time')

    def get_context_data(self, **kwargs):
        context = super(WoodListView, self).get_context_data(**kwargs)
        return context


def form_add(request):
    woods = WoodModel.objects.filter(enable=True).order_by('name')
    types = FORM_TYPE
    return render(request, 'woodform.html', context={'woods': woods, "types": types})


def form_submit(request):
    time = request.POST.get('time')
    wood_id = request.POST.get('name')
    count = int(request.POST.get('count'))
    form_type = int(request.POST.get('type'))
    complete = request.POST.get('complete')
    note = request.POST.get('note')
    wood = WoodModel.objects.get(id=wood_id)
    dic = {"arrive_date": time, "name": wood, "count": count, "type": form_type, "note": note}
    if complete:
        dic["sure"] = complete
        sync_count(wood_id, count, form_type == 1)
    WoodFormModel.objects.create(**dic)
    return HttpResponseRedirect('/home/wood/form/list/')


def form_sure(request):
    return render(request, 'woodformlist.html')


def form_complete(request):
    return render(request, 'woodformlist.html')


def form_delete(request):
    return render(request, 'woodformlist.html')


class WoodFormListView(ListView):
    paginate_by = 15
    model = WoodFormModel
    template_name = 'woodformlist.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        name = self.request.GET.get('name')
        if name:
            id_list = WoodModel.objects.filter(name__contains=name)
            return WoodFormModel.objects.filter(name_id__in=id_list).order_by('-last_mod_time')
        return WoodFormModel.objects.all().order_by('-last_mod_time')

    def get_context_data(self, **kwargs):
        context = super(WoodFormListView, self).get_context_data(**kwargs)
        return context


def sync_count(mid, count, state):
    obj = WoodModel.objects.get(id=mid)
    if state:
        WoodModel.objects.filter(id=mid).update(count=(obj.count + count))
    else:
        WoodModel.objects.filter(id=mid).update(count=(obj.count - count))
