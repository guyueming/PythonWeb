

def nav_list(request):
    func_list = []
    func_list.append(('订单', '/home/wood/list'))
    func_list.append(['销售', '/home/wood/list'])
    func_list.append(('客户', '/home/wood/list'))
    func_list.append(('木料', '/home/wood/list'))
    func_list.append(('纸张', '/home/wood/list'))
    func_list.append(('桉木皮', '/home/wood/list'))
    func_list.append(('钢铁工艺', '/home/wood/list'))
    func_list.append(('规格', '/home/wood/list'))

    return locals()
