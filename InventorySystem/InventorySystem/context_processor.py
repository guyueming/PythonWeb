

def nav_list(request):
    func_list = []
    func_list.append(('订单', '/home/order/head/list'))
    func_list.append(('订单详情', '/home/order/list'))
    func_list.append(('木料', '/home/wood/list'))
    func_list.append(('纸张', '/home/paper/list'))
    func_list.append(('桉木皮|夹板', '/home/skin/list'))
    func_list.append(('客户', '/home/customer/list'))
    func_list.append(['销售', '/home/salesman/list'])
    func_list.append(('钢板工艺', '/home/process/technology/list'))
    func_list.append(('规格', '/home/process/specification/list'))
    return locals()


