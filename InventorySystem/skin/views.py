from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import SkinModel
from account.models import FORM_TYPE
from order.models import SkinFormModel
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


class SkinListView(ListView):
    paginate_by = 15
    model = SkinModel
    template_name = 'skinlist.html'
    context_object_name = 'object_list'

    def get_queryset(self):  # 重写get_queryset方法
        # 获取所有is_deleted为False的用户，并且以时间倒序返回数据
        return SkinModel.objects.filter(enable=True).order_by('-last_mod_time')

    def get_context_data(self, **kwargs):
        context = super(SkinListView, self).get_context_data(**kwargs)
        # context['xxx'] = 'xxx' #添加额外的键值对，传到模板中
        return context

    def GET(self, request):
        search_title = request.GET.get('name')
        SkinModel.objects.filter(name=search_title).order_by('-last_mod_time')


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
    dic = {"arrive_time": time, "name": obj, "count": count, "type": form_type, "note": note}
    if sure:
        dic["sure"] = sure
        update(mid, count, form_type == 1)
    SkinFormModel.objects.create(**dic)
    return HttpResponseRedirect('/home/skin/form/list/')


def update(wood_id, wood_count, add):
    wood = SkinModel.objects.get(id=wood_id)
    if add:
        SkinModel.objects.filter(id=wood_id).update(count=(wood.count + wood_count))
    else:
        SkinModel.objects.filter(id=wood_id).update(count=(wood.count - wood_count))


def form_complete(request):
    return render(request, 'skinform.html')


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


