#!/usr/bin/python
#-*-coding:utf-8-*-
from uuid import uuid4
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import json
# 两个随机颜色都规定不同的区域，防止干扰字符和验证码字符颜色一样
# 随机颜色1:
def rndColor():
    '''
    随机颜色，规定一定范围
    :return:
    '''
    return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))

# 随机颜色2:
def rndColor2():
    '''
      随机颜色，规定一定范围
      :return:
      '''
    return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))
def rnd_char():
    '''
    随机一个字母或者数字
    :return:
    '''
    # 随机一个字母或者数字
    i = random.randint(1,2)
    if i == 1:
        an = random.randint(65, 90)
    elif i == 2:
        an = random.randint(48, 57)
    # 根据Ascii码转成字符，return回去
    return chr(an)


# 两个随机颜色都规定不同的区域，防止干扰字符和验证码字符颜色一样
# 随机颜色1:
def rnd_color():
    '''
    随机颜色，规定一定范围
    :return:
    '''
    return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))

# 随机颜色2:
def rnd_color2():
    '''
      随机颜色，规定一定范围
      :return:
      '''
    return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))

def create_code(codelength,labelList):
    width = 200
    height = 60
    image = Image.new('RGB', (width, height), (random.randint(0,256),random.randint(0,256), random.randint(0,256)))
    # 创建Font对象:
    font = ImageFont.truetype('/home/x/桌面/crnn-pytorch/Fonts/arial.ttf', 36)

    # 创建Draw对象:
    draw = ImageDraw.Draw(image)

    # 填充每个像素:
    for x in range(0, width, 20):
        for y in range(0, height, 10):
            draw.point((x, y), fill=rnd_color())

    # 填充字符
    _str = ""
    # 填入4个随机的数字或字母作为验证码
    for t in range(codelength):
        c = rnd_char()
        _str = "{}{}".format(_str, c)

        # 随机距离图片上边高度，但至少距离30像素
        h = random.randint(1, height-30)
        # 宽度的化，每个字符占图片宽度1／4,在加上10个像素空隙
        w = width/codelength * t
        draw.text((w, h), c, font=font, fill=rnd_color2())

    # 模糊:
    image.filter(ImageFilter.BLUR)
    # uuid1 生成唯一的字符串作为验证码图片名称
    code_name = '{}.jpg'.format(uuid4())
    save_dir = './d/data/{}'.format(code_name)
    image.save(save_dir, 'jpeg')
    dict = {}
    dict['text'] = _str
    dict['name'] = 'data/' +code_name
    labelList.append(dict)

# 当直接运行文件的是和，运行下面代码
if __name__ == "__main__":
    with open("./d/desc.json", 'r') as load_f:
        load_dict = json.load(load_f)
    datasetLength=10
    trainLength=int(datasetLength*0.8)
    testLength=datasetLength-trainLength
    minCodeLength=6
    maxCodeLength=9

    t = load_dict.get('train')
    for i in range(0,trainLength):
        create_code(random.randint(minCodeLength, maxCodeLength),t)
        print('train',i)
    t=load_dict.get('test')
    for i in range(0,testLength):
        create_code(random.randint(minCodeLength,maxCodeLength),t)
        print('test', i)
    with open('./d/desc.json', 'w') as json_file:
        json.dump(load_dict, json_file, ensure_ascii=False)
