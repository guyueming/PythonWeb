from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from wood.models import WoodModel
from skin.models import SkinModel
from paper.models import PaperModel
from customer.models import CustomerModel
from salesman.models import SalesmanModel
from process.models import TechnologyModel, SpecificationModel
from order.models import OrderModel, WoodFormModel
from django.views.generic import ListView


def form_add(request):
    wood_list = WoodModel.objects.filter(enable=True).order_by('name')
    skin_list = SkinModel.objects.filter(enable=True).order_by('name')
    paper_list = PaperModel.objects.filter(enable=True).order_by('name')
    technology_list = TechnologyModel.objects.filter(enable=True).order_by('name')
    specification_list = SpecificationModel.objects.filter(enable=True).order_by('name')
    customer_list = CustomerModel.objects.filter(enable=True).order_by('name')
    salesman_list = SalesmanModel.objects.filter(enable=True).order_by('name')
    return render(request, 'order.html', context={'wood_list': wood_list, 'skin_list': skin_list,
                                                  'paper_list': paper_list, 'technology_list': technology_list,
                                                  'specification_list': specification_list,
                                                  'customer_list': customer_list,
                                                  'salesman_list': salesman_list})


def form_submit(request):
    time = request.POST.get('time')
    wood_id = request.POST.get('wood')
    count = int(request.POST.get('count'))
    form_type = request.POST.get('type')
    complete = request.POST.get('complete')
    wood = WoodModel.objects.get(id=wood_id)
    dic = {"arrive_time": time, "name": wood, "count": count, "type": form_type}
    if complete:
        dic["sure"] = complete
        update(wood_id, count, form_type == 1)
    WoodFormModel.objects.create(**dic)
    return HttpResponseRedirect('/home/order/list/')


def update(wood_id, wood_count, add):
    wood = WoodModel.objects.get(id=wood_id)
    if add:
        WoodModel.objects.filter(id=wood_id).update(count=(wood_count + wood.count))
    else:
        WoodModel.objects.filter(id=wood_id).update(count=(wood.count - wood_count))


def form_complete(request):
    return render(request, 'woodform.html')


class OrderListView(ListView):
    paginate_by = 15
    model = WoodFormModel
    template_name = 'orderlist.html'
    context_object_name = 'object_list'

    def get_queryset(self):  # 重写get_queryset方法
        # 获取所有is_deleted为False的用户，并且以时间倒序返回数据
        return WoodFormModel.objects.all().order_by('-id')

    def get_context_data(self, **kwargs):
        context = super(OrderListView, self).get_context_data(**kwargs)
        # context['xxx'] = 'xxx' #添加额外的键值对，传到模板中
        return context

