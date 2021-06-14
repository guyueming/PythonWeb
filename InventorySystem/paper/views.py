from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import PaperModel
from order.models import FORM_TYPE, PaperFormModel
from django.views.generic import ListView


def add(request):
    return render(request, 'paper.html')


def submit(request):
    name = request.POST.get('name')
    m_type = request.POST.get('type')
    factory = request.POST.get('factory')
    note = request.POST.get('note')
    dic = {"name": name, "type": m_type, "factory": factory, "note": note}
    PaperModel.objects.create(**dic)
    return HttpResponseRedirect('/home/paper/list/')


def enable(request):
    return render(request, 'paperlist.html')


def delete(request):
    return render(request, 'paperlist.html')


class PaperListView(ListView):
    paginate_by = 15
    model = PaperModel
    template_name = 'paperlist.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        return PaperModel.objects.filter(enable=True).order_by('-last_mod_time')

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
    complete = request.POST.get('complete')
    obj = PaperModel.objects.get(id=mid)
    dic = {"arrive_date": time, "name": obj, "count": count, "type": form_type}
    if complete:
        dic["sure"] = complete
        sync_count(mid, count, form_type == 1)
    PaperFormModel.objects.create(**dic)
    return HttpResponseRedirect('/home/paper/form/list/')


def form_sure(request):
    return render(request, 'paperformlist.html')


def form_complete(request):
    return render(request, 'paperformlist.html')


def form_delete(request):
    return render(request, 'paperformlist.html')


class PaperFormListView(ListView):
    paginate_by = 15
    model = PaperFormModel
    template_name = 'paperformlist.html'
    context_object_name = 'object_list'

    def get_queryset(self):  # 重写get_queryset方法
        return PaperFormModel.objects.all().order_by('-last_mod_time')

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

