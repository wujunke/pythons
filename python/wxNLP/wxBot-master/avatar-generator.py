#coding=utf-8
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import random

# 随机大写字母:
def rndChar():
    return chr(random.randint(65, 90))
# 小写
def rndChar2():
    return chr(random.randint(97, 122))
# 随机颜色1:
def rndColor():
    return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))

# 随机颜色2:
def rndColor2():
    return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))



font = ImageFont.truetype('PingFang.ttc', size=50)
letter = unicode(rndChar(),'UTF-8')
(letterWidth, letterHeight) = font.getsize(letter)
imgwidth = 100
imgheight = 100

backcolor = rndColor()
image = Image.new('RGB', (imgwidth, imgheight), backcolor)
    # 创建Draw对象:
draw = ImageDraw.Draw(image)
    # 填充每个像素:
# for x in range(imgwidth):
#     for y in range(imgheight):
#          draw.point((x, y), fill=backcolor)
        # draw.point((x, y))
# 输出文字:
textY0 = (imgheight-letterHeight - 14)/2
textY0 = int(textY0)
textX0 = int((imgwidth-letterWidth)/2)
draw.text((textX0, textY0), letter, font=font, fill=(255,255,255))
# 模糊:
image.save('code.jpg', 'jpeg')