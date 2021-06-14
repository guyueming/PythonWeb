from django.http import HttpResponseRedirect
from django.shortcuts import render
from wood.models import WoodModel
from skin.models import SkinModel
from paper.models import PaperModel
from customer.models import CustomerModel
from salesman.models import SalesmanModel
from process.models import TechnologyModel, SpecificationModel
from order.models import OrderModel, WoodFormModel, SkinFormModel, PaperFormModel
from django.views.generic import ListView
from django.utils.timezone import now


def add(request):
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


def submit(request):
    order_time = request.POST.get('order_time')
    delivery_time = request.POST.get('delivery_time')
    count = int(request.POST.get('count'))
    salesman_id = request.POST.get('salesman')
    customer_id = request.POST.get('customer')
    wood_id = request.POST.get('wood')
    wood_count = int(request.POST.get('wood_count'))
    skin_id = request.POST.get('skin')
    skin_count = int(request.POST.get('skin_count'))
    paper_id = request.POST.get('paper')
    paper_count = int(request.POST.get('paper_count'))
    technology_id = request.POST.get('technology')
    specification_id = request.POST.get('specification')
    color = request.POST.get('color')
    packaging = request.POST.get('package')
    thickness = request.POST.get('thickness')
    trademark = request.POST.get('trademark')
    word = request.POST.get('word')
    note = request.POST.get('note')
    grooving = request.POST.get('grooving')
    drying = request.POST.get('drying')
    sure = request.POST.get('sure')
    salesman = SalesmanModel.objects.get(id=salesman_id)
    customer = CustomerModel.objects.get(id=customer_id)
    wood = WoodModel.objects.get(id=wood_id)
    skin = SkinModel.objects.get(id=skin_id)
    paper = PaperModel.objects.get(id=paper_id)
    technology = TechnologyModel.objects.get(id=technology_id)
    specifications = SpecificationModel.objects.get(id=specification_id)
    dic = {"order_date": order_time, "delivery_date": delivery_time, "count": count,
           "salesman": salesman, "customer": customer,
           "wood": wood, "woodCount": wood_count, "skin": skin, "skinCount": skin_count,
           "paper": paper, "paperCount": paper_count,
           "technology": technology if technology else False,
           "specifications": specifications if technology else False,
           "color": color, "packaging": packaging, "thickness": thickness,
           "trademark": trademark, "word": word, "note": note,
           "is_grooving": grooving if grooving else False,
           "is_drying": drying if drying else False,
           "sure": sure if sure else False,
           }
    order = OrderModel.objects.create(**dic)
    if sure:
        sync_form_wood(order, wood, wood_count)
        sync_form_skin(order, skin, skin_count)
        sync_form_paper(order, paper, wood_count)
    return HttpResponseRedirect('/home/order/list/')


def make_edit(request):
    return render(request, 'order.html')


def make_sure(request):
    return render(request, 'orderlist.html')


def make_complete(request):
    return render(request, 'orderlist.html')


def make_delete(request):
    return render(request, 'orderlist.html')


class OrderListView(ListView):
    paginate_by = 6
    model = OrderModel
    template_name = 'orderlist.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        return OrderModel.objects.all().order_by('-id')

    def get_context_data(self, **kwargs):
        context = super(OrderListView, self).get_context_data(**kwargs)
        # context['xxx'] = 'xxx' #添加额外的键值对，传到模板中
        return context


def sync_form_wood(order, wood, count):
    dic = {"name": wood, "count": count, "type": 4, "order": order}
    WoodFormModel.objects.create(**dic)
    wood.count -= count
    wood.save()


def sync_form_skin(order, skin, count):
    dic = {"name": skin, "count": count, "type": 4, "order": order}
    SkinFormModel.objects.create(**dic)
    skin.count -= count
    skin.save()


def sync_form_paper(order, paper, count):
    dic = {"name": paper, "count": count, "type": 4, "order": order}
    PaperFormModel.objects.create(**dic)
    paper.count -= count
    paper.save()

