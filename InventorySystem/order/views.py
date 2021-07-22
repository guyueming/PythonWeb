import time
from django.contrib import messages
from django.db.models import Q
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
from .forms import OrderHeadForm, OrderFormSet, ViewOrderFormSet


def add_order(request, pk):
    head = OrderHeadModel.objects.get(id=pk)
    if request.method == "GET":
        wood_list = WoodModel.objects.filter(enable=True).order_by('name')
        skin_list = SkinModel.objects.filter(enable=True).order_by('name')
        paper_list = PaperModel.objects.filter(enable=True).order_by('color')
        technology_list = TechnologyModel.objects.filter(enable=True).order_by('name')
        specification_list = SpecificationModel.objects.filter(enable=True).order_by('name')
        return render(request, 'order.html', context={'wood_list': wood_list, 'skin_list': skin_list,
                                                      'paper_list': paper_list, 'technology_list': technology_list,
                                                      'specification_list': specification_list, 'head': head, })
    else:
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
        wood = WoodModel.objects.get(id=wood_id)
        technology = TechnologyModel.objects.get(id=technology_id)
        specifications = SpecificationModel.objects.get(id=specification_id)
        dic = {"head_number": head,
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

        other_skin_id = request.POST.get('other_skin')
        if other_skin_id:
            other_skin = SkinModel.objects.get(id=other_skin_id)
            other_skin_count = int(request.POST.get('other_skin_count'))
            dic["other_skin"] = other_skin
            dic["other_skin_count"] = other_skin_count

        paper_name = request.POST.get('paper')
        paper = PaperModel.objects.first_item(paper_name)
        if paper:
            paper_count = int(request.POST.get('paper_count'))
            dic["paper"] = paper
            dic["paperCount"] = paper_count

        other_paper_name = request.POST.get('other_paper')
        other_paper = PaperModel.objects.first_item(other_paper_name)
        if other_paper:
            other_paper_count = int(request.POST.get('other_paper_count'))
            dic["other_paper"] = other_paper
            dic["other_paper_count"] = other_paper_count

        order = OrderModel.objects.create(**dic)
        if order:
            sync_material_count(order)
        else:
            messages.success(request, "创建失败")
        return HttpResponseRedirect('/home/order/list/')


def get_order_number():
    date = int(time.strftime("%Y%m%d", time.localtime()))
    try:
        number = OrderNumberModel.objects.get(order_date=date)
    except OrderNumberModel.DoesNotExist:
        dic = {"order_date": date, "order_number": 0}
        number = OrderNumberModel.objects.create(**dic)

    if number.order_number > 9999:
        return 0

    number.order_number += 1
    number.save()
    order_number = date * 10000 + number.order_number
    return order_number


def add_orders(request):
    if request.method == "POST":
        form = OrderHeadForm(request.POST)
        products = []
        success = True
        if form.is_valid():
            order_head = form.save(commit=False)
            formset = OrderFormSet(request.POST, instance=order_head)
            for order in formset:
                if order.is_valid():
                    model = order.save(commit=False)
                    products.append(model)
                else:
                    success = False
                    print(order)
            if success:
                order_head.save()
                for item in products:
                    item.save()
                    update_sure_state(item.id, True)
                return HttpResponseRedirect('/home/order/list/')
    else:
        form = OrderHeadForm(initial={'order_number': get_order_number()})
        formset = OrderFormSet()
    return render(request, 'orders.html', {'form': form, 'formset': formset, })


def view_orders(request, pk):
    if request.method == "POST":
        form = OrderHeadForm(request.POST)
        if form.is_valid():
            order_head = form.save()
            formset = ViewOrderFormSet(request.POST, instance=order_head)
            if formset.is_valid():
                formset.save()
    else:
        print("pk", pk)
        order_heads = OrderHeadModel.objects.filter(id=pk)
        if order_heads and len(order_heads) > 0:
            form = OrderHeadForm(instance=order_heads[0])
            formset = ViewOrderFormSet(instance=order_heads[0])
            return render(request, 'order_view.html', {'form': form, 'formset': formset, })

    return HttpResponseRedirect('/home/order/list/')


def view_detail_orders(request, pk):
    detail = OrderModel.objects.filter(id=pk).first()
    if detail:
        order_heads = OrderHeadModel.objects.filter(id=detail.head_number.id)
        if order_heads and len(order_heads) > 0:
            form = OrderHeadForm(instance=order_heads[0])
            formset = ViewOrderFormSet(instance=order_heads[0])
            return render(request, 'order_view.html', {'form': form, 'formset': formset, })
    return HttpResponseRedirect('/home/order/list/')


def edit_orders(request, pk):
    try:
        order_head = OrderHeadModel.objects.get(id=pk)
    except OrderHeadModel.DoesNotExist:
        return HttpResponseRedirect('/home/order/list/')

    if request.method == "POST":
        form = OrderHeadForm(request.POST, instance=order_head)
        formset = ViewOrderFormSet(request.POST, instance=order_head)
        if form.is_valid() and formset.is_valid():
            products = []
            success = True
            for item in formset:
                if item.is_valid() and item.has_changed():
                    print('test', len(products))
                    products.append(item)
                else:
                    success = False
            if success:
                if form.has_changed():
                    form.save()
                for item in products:
                    model = item.save(commit=False)
                    if model.id:
                        update_sure_state(model.id, False)
                    model.save()
                    update_sure_state(model.id, True)
                return HttpResponseRedirect('/home/order/list/')
    else:
        form = OrderHeadForm(instance=order_head)
        formset = ViewOrderFormSet(instance=order_head)
    return render(request, 'orders.html', {'form': form, 'formset': formset, })


def make_sure(request):
    obj_id = request.GET.get('id')
    update_sure_state(obj_id)
    return HttpResponseRedirect('/home/order/list/')


def make_head_sure(request):
    obj_id = request.GET.get('id')
    update_head_sure_state(obj_id)
    return HttpResponseRedirect('/home/order/list/')


def make_head_complete(request):
    obj_id = request.GET.get('id')
    orders = OrderModel.objects.filter(head_number=obj_id)
    for item in orders:
        if not item.sure:
            messages.success(request, "请先确认所有数据")
            return HttpResponseRedirect('/home/order/head/list/')
    obj = OrderHeadModel.objects.get(id=obj_id)
    obj.complete = not obj.complete
    obj.save()
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
    form = OrderHeadModel.objects.get(id=obj_id)
    if form.sure:
        messages.success(request, "请先取消确认")
    try:
        OrderHeadModel.objects.filter(id=obj_id).delete()
    except Exception as e:
        messages.success(request, e.args)
    return HttpResponseRedirect('/home/order/head/list/')


class OrderListView(ListView):
    paginate_by = 12
    model = OrderModel
    template_name = 'orderlist.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        q = Q()
        # customer = self.request.GET.get('customer')
        # if customer:
        #     id_list = CustomerModel.objects.filter(name__icontains=customer)
        #     q.add(Q(customer__in=id_list), Q.AND)
        # wood = self.request.GET.get('wood')
        # if wood:
        #     id_list = WoodModel.objects.filter(name__icontains=wood)
        #     q.add(Q(wood__in=id_list), Q.AND)
        papers = self.request.GET.get('paper')
        if papers:
            id_list = PaperModel.objects.query_str(papers)
            q.add(Q(paper__in=id_list), Q.OR)
            q.add(Q(other_paper__in=id_list), Q.OR)
        # skins = self.request.GET.get('skin')
        # if skins:
        #     id_list = SkinModel.objects.filter(name__icontains=wood)
        #     q.add(Q(skin__in=id_list), Q.OR)
        #     q.add(Q(other_skin__in=id_list), Q.OR)
        return OrderModel.objects.filter(q).order_by('-id')

    def get_context_data(self, **kwargs):
        context = super(OrderListView, self).get_context_data(**kwargs)
        return context


class OrderHeadListView(ListView):
    paginate_by = 16
    model = OrderModel
    template_name = 'orderheadlist.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        return OrderHeadModel.objects.all().order_by('-id')

    def get_context_data(self, **kwargs):
        context = super(OrderHeadListView, self).get_context_data(**kwargs)
        return context


def update_sure_state(obj_id, state=None):
    obj = OrderModel.objects.get(id=obj_id)
    if obj.sure == state:
        return
    if state:
        obj.sure = state
    else:
        obj.sure = not obj.sure
    obj.save()
    sync_material_count(obj)


def update_head_sure_state(obj_id):
    obj = OrderHeadModel.objects.get(id=obj_id)
    print(obj)


def sync_material_count(order):
    sync_form_wood(order, order.wood, order.woodCount, order.sure)
    sync_form_skin(order, order.skin, order.skinCount, order.sure)
    sync_form_skin(order, order.other_skin, order.other_skin_count, order.sure)
    sync_form_paper(order, order.paper, order.paperCount, order.sure)
    sync_form_paper(order, order.other_paper, order.other_paper_count, order.sure)


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
