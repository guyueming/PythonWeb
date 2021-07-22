import os
import time

import xlwt
from paper.models import PaperModel


def expert():
    workbook = xlwt.Workbook()
    papers = PaperModel.objects.all().order_by('factory', '-count')
    factory = ''
    worksheet = None
    index = 0
    for item in papers:
        if factory != item.factory:
            factory = item.factory
            index = 0
            worksheet = workbook.add_sheet(factory)
        worksheet.write(index, 0, item.color)
        worksheet.write(index, 1, item.type)
        worksheet.write(index, 3, item.count)
        index += 1

    # 添加公式
    # worksheet.write(1, 0, xlwt.Formula('A1*B1')) # Should output "10" (A1[5] * A2[2])
    # worksheet.write(1, 1, xlwt.Formula('SUM(A1,B1)')) # Should output "7" (A1[5] + A2[2])

    from io import BytesIO
    output = BytesIO()
    workbook.save(output)
    # 重新定位到开始
    output.seek(0)
    return output.getvalue()
