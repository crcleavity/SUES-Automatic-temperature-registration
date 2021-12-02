import random
import os
from PIL import Image, ImageDraw, ImageFont

width = 70
height = 32


def getRandomColor(is_light=True):
    """
    生成随机颜色
    :param is_light: 为了设置浅色和深色
    :return:  (r, g, b)
    """
    r = random.randint(0, 127) + int(is_light) * 128
    g = random.randint(0, 127) + int(is_light) * 128
    b = random.randint(0, 127) + int(is_light) * 128
    return r, g, b


def getRandomChar():
    random_num = str(random.randint(0, 9))
    # random_lower = chr(random.randint(97, 122))
    # random_upper = chr(random.randint(65, 90))
    # random_char = random.choice([random_num, random_upper])
    return random_num


def drawLine(draw):
    """
    随机生成4个干扰线，然后每个设置随机颜色
    """
    for i in range(3):
        x1 = random.randint(0, width)
        x2 = random.randint(0, width)
        y1 = random.randint(0, height)
        y2 = random.randint(0, height)
        # draw.line((x1, y1, x2, y2), fill=getRandomColor(is_light=True))
        draw.line((x1, y1, x2, y2), fill=(0, 0, 0))

        x1 = random.randint(0, width)
        x2 = random.randint(0, width)
        y1 = random.randint(0, height)
        y2 = random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=(255, 255, 255))


def drawPoint(draw):
    """
    随机生成80个干扰点，然后每个设置随机颜色
    """
    for i in range(80):
        x = random.randint(0, width)
        y = random.randint(0, height)
        # draw.point((x, y), fill=getRandomColor(is_light=True))
        draw.point((x, y), fill=(0, 0, 0))

        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.point((x, y), fill=(255, 255, 255))


def createImg(folder):
    # bg_color = getRandomColor(is_light=False)
    bg_color = 255, 255, 255
    img = Image.new(mode="RGB", size=(width, height), color=bg_color)
    draw = ImageDraw.Draw(img)
    file_name = ''

    for i in range(4):
        random_txt = getRandomChar()
        # txt_color = getRandomColor(is_light=False)
        txt_color = 0, 0, 0
        # while txt_color == bg_color:
        #     txt_color = getRandomColor(is_light=False)

        my_font = ImageFont.truetype("./simhei.ttf", size=28)
        a = random.randint(-2, 2)
        b = random.randint(-1, 1)
        draw.text((5 + 16 * i + a, 1 + b), text=random_txt, font=my_font, fill=txt_color, fontweight='bold')
        file_name += random_txt

    drawLine(draw)
    drawPoint(draw)

    with open("./{}/{}.png".format(folder, file_name), "wb") as f:
        img = img.convert('L')
        count = 255
        table = []
        for i in range(256):
            if i < count:
                table.append(0)
            else:
                table.append(1)

        img = img.point(table, '1')
        img.save(f, format="png")


if __name__ == '__main__':
    num = 10000

    os.path.exists('train') or os.makedirs('train')
    os.path.exists('test') or os.makedirs('test')

    for _ in range(num):
        createImg('train')
        createImg('test')
