from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from wood.models import WoodModel
from skin.models import SkinModel
from paper.models import PaperModel
from customer.models import CustomerModel
from salesman.models import SalesmanModel
from process.models import TechnologyModel, SpecificationModel
from order.models import OrderModel, WoodFormModel, SkinFormModel, PaperFormModel, OrderNumberModel, OrderHeadModel
from django.views.generic import ListView
from .forms import OrderHeadForm, OrderFormSet


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


def add_orders(request):  # 创建
    if request.method == "POST":
        form = OrderHeadForm(request.POST)

        if form.is_valid():
            order_head = form.save()
            formset = OrderFormSet(request.POST, instance=order_head)
            if formset.is_valid():
                formset.save()
            print(formset)
        return HttpResponseRedirect('/home/order/list/')
    else:
        form = OrderHeadForm()
        formset = OrderFormSet()

    return render(request, 'orders.html', {'form': form, 'formset': formset, })


# def add_orders(request):
#     wood_list = WoodModel.objects.filter(enable=True).order_by('name')
#     skin_list = SkinModel.objects.filter(enable=True).order_by('name')
#     paper_list = PaperModel.objects.filter(enable=True).order_by('name')
#     technology_list = TechnologyModel.objects.filter(enable=True).order_by('name')
#     specification_list = SpecificationModel.objects.filter(enable=True).order_by('name')
#     customer_list = CustomerModel.objects.filter(enable=True).order_by('name')
#     salesman_list = SalesmanModel.objects.filter(enable=True).order_by('name')
#     order_list = [1, 2, 3]
#     return render(request, 'orders.html', context={'wood_list': wood_list, 'skin_list': skin_list,
#                                                    'paper_list': paper_list, 'technology_list': technology_list,
#                                                    'specification_list': specification_list,
#                                                    'customer_list': customer_list,
#                                                    'salesman_list': salesman_list, "list": order_list})


def submit(request):
    order_number = request.POST.get('order_number')
    order_time = request.POST.get('order_time')
    delivery_time = request.POST.get('delivery_time')
    salesman_id = request.POST.get('salesman')
    customer_id = request.POST.get('customer')
    wood_id = request.POST.get('wood')
    wood_count = int(request.POST.get('wood_count'))
    technology_id = request.POST.get('technology')
    specification_id = request.POST.get('specification')
    packaging = request.POST.get('package')
    thickness = request.POST.get('thickness')
    trademark = request.POST.get('trademark')
    word = request.POST.get('word')
    note = request.POST.get('note')
    grooving = request.POST.get('grooving')
    drying = request.POST.get('drying')
    salesman = SalesmanModel.objects.get(id=salesman_id)
    customer = CustomerModel.objects.get(id=customer_id)
    wood = WoodModel.objects.get(id=wood_id)
    technology = TechnologyModel.objects.get(id=technology_id)
    specifications = SpecificationModel.objects.get(id=specification_id)
    order_dic = {"order_number": order_number, "order_date": order_time, "delivery_date": delivery_time,
                 "salesman": salesman, "customer": customer}
    order_head = OrderHeadModel.objects.create(**order_dic)
    dic = {"head_number": order_head,
           "wood": wood, "woodCount": wood_count,
           "technology": technology, "specifications": specifications,
           "packaging": packaging, "thickness": thickness,
           "trademark": trademark, "word": word, "note": note,
           "is_grooving": grooving if grooving else False,
           "is_drying": drying if drying else False,
           "sure": True,
           }
    skin_id = request.POST.get('skin')
    if skin_id:
        skin = SkinModel.objects.get(id=skin_id)
        skin_count = int(request.POST.get('skin_count'))
        dic["skin"] = skin
        dic["skinCount"] = skin_count

    paper_id = request.POST.get('paper')
    if paper_id:
        paper = PaperModel.objects.get(id=paper_id)
        paper_count = int(request.POST.get('paper_count'))
        dic["paper"] = paper
        dic["paperCount"] = paper_count

    other_paper_id = request.POST.get('other_paper')
    if other_paper_id:
        other_paper = PaperModel.objects.get(id=other_paper_id)
        other_paper_count = int(request.POST.get('other_paper_count'))
        dic["other_paper"] = other_paper
        dic["other_paper_count"] = other_paper_count

    order = OrderModel.objects.create(**dic)
    if order:
        sync_form_wood(order, order.wood, order.woodCount, True)
        sync_form_skin(order, order.skin, order.skinCount, True)
        sync_form_paper(order, order.paper, order.paperCount, True)
        sync_form_paper(order, order.other_paper, order.other_paper_count, True)
    else:
        messages.success(request, "创建失败")
    return HttpResponseRedirect('/home/order/list/')


def submit_order_list(request):
    order = request.POST.get("table")
    print(order)
    return HttpResponseRedirect('/home/order/list/')


def make_edit(request):
    return HttpResponseRedirect('/home/order/list/')


def make_sure(request):
    obj_id = request.GET.get('id')
    obj = OrderModel.objects.get(id=obj_id)
    obj.sure = not obj.sure
    sync_material_count(obj)
    obj.save()
    return HttpResponseRedirect('/home/order/list/')


def make_complete(request):
    return HttpResponseRedirect('/home/order/list/')


def make_head_complete(request):
    return HttpResponseRedirect('/home/order/head/list/')


def make_delete(request):
    obj_id = request.GET.get('id')
    form = OrderModel.objects.get(id=obj_id)
    if form.sure:
        messages.success(request, "请先取消确认")
    else:
        try:
            OrderModel.objects.filter(id=obj_id).delete()
        except Exception as e:
            messages.success(request, e.args)
    return HttpResponseRedirect('/home/order/list/')


def make_head_delete(request):
    obj_id = request.GET.get('id')
    try:
        OrderHeadModel.objects.filter(id=obj_id).delete()
    except Exception as e:
        messages.success(request, e.args)
    return HttpResponseRedirect('/home/order/head/list/')


class OrderListView(ListView):
    paginate_by = 10
    model = OrderModel
    template_name = 'orderlist.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        return OrderModel.objects.all().order_by('-id')

    def get_context_data(self, **kwargs):
        context = super(OrderListView, self).get_context_data(**kwargs)
        return context


class OrderHeadListView(ListView):
    paginate_by = 10
    model = OrderModel
    template_name = 'orderheadlist.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        return OrderHeadModel.objects.all().order_by('-id')

    def get_context_data(self, **kwargs):
        context = super(OrderHeadListView, self).get_context_data(**kwargs)
        return context


def sync_material_count(order):
    wood = order.wood
    skin = order.skin
    paper = order.paper
    other_paper = order.other_paper

    sync_form_wood(order, wood, order.woodCount, order.sure)
    sync_form_skin(order, skin, order.skinCount, order.sure)
    sync_form_paper(order, paper, order.paperCount, order.sure)
    sync_form_paper(order, other_paper, order.other_paper_count, order.sure)


def sync_form_wood(order, wood, count, sure):
    if not wood:
        return
    if sure:
        dic = {"name": wood, "count": count, "type": 4, "order": order}
        WoodFormModel.objects.create(**dic)
        wood.count -= count
        wood.save()
    else:
        WoodFormModel.objects.filter(order=order).delete()
        wood.count += count
        wood.save()


def sync_form_skin(order, skin, count, sure):
    if not skin:
        return
    if sure:
        dic = {"name": skin, "count": count, "type": 4, "order": order}
        SkinFormModel.objects.create(**dic)
        skin.count -= count
        skin.save()
    else:
        SkinFormModel.objects.filter(order=order).delete()
        skin.count += count
        skin.save()


def sync_form_paper(order, paper, count, sure):
    if not paper:
        return
    if sure:
        dic = {"name": paper, "count": count, "type": 4, "order": order}
        PaperFormModel.objects.create(**dic)
        paper.count -= count
        paper.save()
    else:
        PaperFormModel.objects.filter(order=order).delete()
        paper.count += count
        paper.save()

