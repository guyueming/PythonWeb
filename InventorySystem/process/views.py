from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import TechnologyModel, SpecificationModel
from django.views.generic import ListView
from django.contrib import messages


def technology_add(request):
    return render(request, 'technology.html')


def technology_submit(request):
    name = request.POST.get('name')
    note = request.POST.get('note')
    dic = {"name": name, "note": note}
    TechnologyModel.objects.create(**dic)
    return HttpResponseRedirect('/home/process/technology/list/')


def technology_enable(request):
    obj_id = request.GET.get('id')
    obj = TechnologyModel.objects.get(id=obj_id)
    obj.enable = not obj.enable
    obj.save()
    return HttpResponseRedirect('/home/process/technology/list/')


def technology_delete(request):
    obj_id = request.GET.get('id')
    try:
        TechnologyModel.objects.filter(id=obj_id).delete()
    except Exception as e:
        messages.success(request, e.args)
    return HttpResponseRedirect('/home/process/technology/list/')


class TechnologyListView(ListView):
    paginate_by = 15
    model = TechnologyModel
    template_name = 'technologylist.html'
    context_object_name = 'object_list'

    def get_queryset(self):  # 重写get_queryset方法
        return TechnologyModel.objects.all().order_by('-id')

    def get_context_data(self, **kwargs):
        context = super(TechnologyListView, self).get_context_data(**kwargs)
        # context['xxx'] = 'xxx' #添加额外的键值对，传到模板中
        return context


def specification_add(request):
    return render(request, 'specification.html')


def specification_submit(request):
    name = request.POST.get('name')
    note = request.POST.get('note')
    dic = {"name": name, "note": note}
    SpecificationModel.objects.create(**dic)
    return HttpResponseRedirect('/home/process/specification/list/')


def specification_enable(request):
    obj_id = request.GET.get('id')
    obj = SpecificationModel.objects.get(id=obj_id)
    obj.enable = not obj.enable
    obj.save()
    return HttpResponseRedirect('/home/process/specification/list/')


def specification_delete(request):
    obj_id = request.GET.get('id')
    try:
        SpecificationModel.objects.filter(id=obj_id).delete()
    except Exception as e:
        messages.success(request, e.args)
    return HttpResponseRedirect('/home/process/specification/list/')


class SpecificationListView(ListView):
    paginate_by = 15
    model = SpecificationModel
    template_name = 'specificationlist.html'
    context_object_name = 'object_list'

    def get_queryset(self):  # 重写get_queryset方法
        # 获取所有is_deleted为False的用户，并且以时间倒序返回数据
        return SpecificationModel.objects.all().order_by('-id')

    def get_context_data(self, **kwargs):
        context = super(SpecificationListView, self).get_context_data(**kwargs)
        # context['xxx'] = 'xxx' #添加额外的键值对，传到模板中
        return context
