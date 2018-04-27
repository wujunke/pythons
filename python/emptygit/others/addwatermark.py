#coding=utf8
import os

from PyPDF2 import PdfFileReader
from PyPDF2 import PdfFileWriter
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A1,A0, A4


def addWaterMark(pdfpath='742.pdf',watermarkcontent='多维海拓'):
    print datetime.now()
    pdfmetrics.registerFont(TTFont('song', '/Library/Fonts/Arial Unicode.ttf'))
    watermarkpath = pdfpath.split('.')[0] + '-water' + '.pdf'
    out_path = pdfpath.split('.')[0] + '-out' + '.pdf'
    c = canvas.Canvas(watermarkpath,A1)
    # 设置字体
    c.setFont("song", 20)
    # 旋转45度，坐标系被旋转
    # 旋转45度，坐标系被旋转
    c.rotate(45)
    c.translate(0,-A1[1] * 0.5)
    # 设置透明度，1为不透明
    watermarkcontent = ['多维海拓一', 'fadasdafs', 'fadasdafs']
    width0 = c.stringWidth(text=watermarkcontent[0], fontName='song', fontSize=20)
    width1 = c.stringWidth(text=watermarkcontent[1], fontName='song', fontSize=20)
    width2 = c.stringWidth(text=watermarkcontent[2], fontName='song', fontSize=20)
    print  width0,width1,width2
    y = 0
    while y < A1[1]:
        x = 100
        while x < A1[0]:
            c.setFillAlpha(0.05)
            c.drawCentredString(x, y, watermarkcontent[0])
            print x
            x = x + width0 *2
            c.drawCentredString(x, y, watermarkcontent[1])
            print x
            x = x + width1 *2
            c.drawCentredString(x, y, watermarkcontent[2])
            print x
            x = x + width2 *2
        y += 60

    # c.setFillAlpha(0.05)
    # c.drawCentredString((x - 3) * cm, (y - 3) * cm, watermarkcontent)
    # c.setFillAlpha(0.05)
    # c.drawCentredString(x * cm, y * cm, watermarkcontent)
    # c.setFillAlpha(0.05)
    # c.drawCentredString((x + 3) * cm, (y + 3) * cm, watermarkcontent)
    c.save()
    watermark = PdfFileReader(open(watermarkpath, "rb"))

    # Get our files ready
    output_file = PdfFileWriter()
    input_file = PdfFileReader(open(pdfpath, "rb"))
    page_count = input_file.getNumPages()
    for page_number in range(page_count):
        input_page = input_file.getPage(page_number)
        input_page.mergePage(watermark.getPage(0))
        output_file.addPage(input_page)
    with open(out_path, "wb") as outputStream:
        output_file.write(outputStream)
    # os.remove(watermarkpath)
    print datetime.now()
    return out_path

addWaterMark()