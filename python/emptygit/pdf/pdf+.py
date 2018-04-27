# coding: utf-8
# pdf_watermark.py
import traceback

import datetime
from reportlab.lib.units import cm, inch
from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileWriter, PdfFileReader

# # Create the watermark from an image
# c = canvas.Canvas('watermark.pdf')
# 移动坐标原点(坐标系左下为(0,0))
# c.translate(10 * cm, 5 * cm)
#
# # 设置字体
# c.setFont("Helvetica", 80)
# # 指定描边的颜色
# c.setStrokeColorRGB(0, 1, 0)
# # 指定填充颜色
# c.setFillColorRGB(0, 1, 0)
# # 画一个矩形
# c.rect(cm, cm, 7 * cm, 17 * cm, fill=1)
#
# # 旋转45度，坐标系被旋转
# c.rotate(45)
# # 指定填充颜色
# c.setFillColorRGB(0.6, 0, 0)
# # 设置透明度，1为不透明
# c.setFillAlpha(0.3)
# # 画几个文本，注意坐标系旋转的影响
# c.drawString(3 * cm, 0 * cm, content)
# c.setFillAlpha(0.6)
# c.drawString(6 * cm, 3 * cm, content)
# c.setFillAlpha(1)
# c.drawString(9 * cm, 6 * cm, content)
#
# # 关闭并保存pdf文件
# c.save()
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('song', '/Library/Fonts/AppleGothic.ttf'))
# pdfmetrics.registerFont(TTFont('song', 'aaaa.ttf'))



from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

x = 16
y = 1
def create_watermark(content):
    # 默认大小为21cm*29.7cm
    c = canvas.Canvas("mark.pdf")
    # 移动坐标原点(坐标系左下为(0,0))
    # c.translate(5 * cm, 0 * cm)
    print cm
    print c._pagesize
    for xx in c._pagesize:
        print xx/cm
    # 设置字体
    c.setFont("song", 40)
    # # 指定描边的颜色
    # c.setStrokeColorRGB(0, 1, 0)
    # # 指定填充颜色
    # c.setFillColorRGB(0, 1, 0)
    # # 画一个矩形
    # c.rect(0, 0, 29.7 * cm, 21.0 * cm, fill=1)

    # 旋转45度，坐标系被旋转
    c.rotate(45)
    # 指定填充颜色
    c.setFillColorRGB(0.6, 0, 0)
    # 设置透明度，1为不透明
    c.setFillAlpha(0.3)
    c.drawCentredString((x - 3) * cm, (y - 3) * cm, content)
    c.setFillAlpha(0.3)
    c.drawCentredString(x * cm,  y * cm, content)
    c.setFillAlpha(0.3)
    c.drawCentredString((x + 3) * cm, (y + 3) * cm, content)

    # 关闭并保存pdf文件
    c.save()

# create_watermark('aaaaa@investarget.com')





# from reportlab.pdfgen import canvas
# from reportlab.pdfbase import pdfmetrics
# from reportlab.pdfbase.ttfonts import TTFont
# aa = pdfmetrics.getRegisteredFontNames()
# print aa
# # 设置绘画开始的位置
# def hello(c):
#     c.drawString(100, 100, "您好")
#     width = c.stringWidth("您好")
#     c.drawString(100, 120, "文本宽度:%f"%width)
# #定义要生成的pdf的名称
# c=canvas.Canvas("hello.pdf")
# #设置字体
# c.setFont("ZapfDingbats", 8)
# #调用函数进行绘画，并将canvas对象作为参数传递
# hello(c)
# #showPage函数：保存当前页的canvas
# c.showPage()
# #save函数：保存文件并关闭canvas
# c.save()










def sendPDF(request):
    try:
        options = {
                'dpi': 1400,
                'page-size': 'A4',
                'margin-top': '0.75in',
                'margin-right': '0.75in',
                'margin-bottom': '0.75in',
                'margin-left': '0.75in',
                'encoding': "UTF-8",
                'no-outline': None,
            }
        pdfpath = '/Users/investarget/' + 'P' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.pdf'
        config = pdfkit.configuration(wkhtmltopdf=APILOG_PATH['wkhtmltopdf'])
        aaa = pdfkit.from_url(PROJECTPDF_URLPATH + str(proj.id)+'&lang=%s'%lang, pdfpath, configuration=config, options=options)
        out_path = addWaterMark(pdfpath,watermarkcontent=[request.user.usernameC, request.user.org.orgnameC if request.user.org else request.user.email, request.user.email])
        if aaa:
                # fn = open(out_path, 'rb')
                # response = StreamingHttpResponse(file_iterator(fn))
                # response['Content-Type'] = 'application/octet-stream'
                # response["content-disposition"] = 'attachment;filename=%s.pdf'% (proj.projtitleC.encode('utf-8') if lang == 'cn' else proj.projtitleE)
                # os.remove(out_path)
            print 'ok'
        else:
            print 'error'
        print 'ok'
    except Exception:
        print traceback.format_exc().split('\n')[-2]


