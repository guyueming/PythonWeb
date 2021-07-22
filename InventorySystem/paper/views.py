import time

from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from order import make_excel
from .forms import PaperForm
from .models import PaperModel
from order.models import FORM_TYPE, PaperFormModel
from django.views.generic import ListView


def add(request):
    if request.method == 'POST':
        form = PaperForm(request.POST)
        if form.is_valid():
            dic = {"color": form.cleaned_data['color'],
                   "type": form.cleaned_data['type'],
                   "factory": form.cleaned_data['factory'],
                   "note": form.cleaned_data['note'],
                   "count": form.cleaned_data['count']}
            PaperModel.objects.create(**dic)
            return HttpResponseRedirect('/home/paper/list/')
    else:
        form = PaperForm()
    return render(request, 'paper.html', {'form': form})


def submit(request):
    model = request.POST.get('model')
    factory = request.POST.get('factory')
    color = request.POST.get('color')
    note = request.POST.get('note')
    dic = {"type": model, "factory": factory, "note": note, "color": color}
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


def output(request):

    date = time.localtime()
    filename = time.strftime("%Y-%m-%d %H:%M", date)
    path = filename + '.xls'
    # response = StreamingHttpResponse(file_iterator(path[0]))
    response = HttpResponse(content_type='application/vnd.ms-excel')
    # response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(path)
    response.write(make_excel.expert())
    return response


class PaperListView(ListView):
    paginate_by = 15
    model = PaperModel
    template_name = 'paperlist.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        q = Q()
        name = self.request.GET.get('name')
        if name:
            q.add(Q(color__icontains=name), Q.OR)
            q.add(Q(type__icontains=name), Q.OR)
            q.add(Q(factory__icontains=name), Q.OR)
        return PaperModel.objects.filter(q).order_by('color')

    def get_context_data(self, **kwargs):
        context = super(PaperListView, self).get_context_data(**kwargs)
        # context['xxx'] = 'xxx' #添加额外的键值对，传到模板中
        return context


def form_add(request):
    q = Q(enable=True)
    obj_id = request.GET.get('id')
    if obj_id:
        q.add(Q(id=obj_id), Q.AND)
    object_list = PaperModel.objects.filter(q).order_by('color')
    types = FORM_TYPE
    return render(request, 'paperform.html', context={'object_list': object_list, "types": types})


def form_submit(request):
    time = request.POST.get('time')
    count = int(request.POST.get('count'))
    form_type = int(request.POST.get('type'))
    obj = request.POST.get('name')
    name = PaperModel.objects.first_item(obj)
    if name:
        dic = {"arrive_date": time, "name": name, "count": count, "type": form_type, "sure": True}
        success = PaperFormModel.objects.create(**dic)
        if success:
            sync_count(name.id, count, form_type == 1)
        return HttpResponseRedirect('/home/paper/form/list/')
    else:
        messages.success(request, "纸张选择错误")
    return HttpResponseRedirect('/home/paper/form/list/')


def form_sure(request):
    obj_id = request.GET.get('id')
    obj = PaperFormModel.objects.get(id=obj_id)
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
        q = Q()
        obj_id = self.request.GET.get('id')
        if obj_id:
            q.add(Q(name_id=obj_id), Q.AND)
        else:
            id_list = PaperModel.objects.query_str(self.request.GET.get('name'))
            q.add(Q(name__in=id_list), Q.OR)

        return PaperFormModel.objects.filter(q).order_by('-id')

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
