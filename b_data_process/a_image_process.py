#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/22 0022 上午 10:46
# @Author  : Lovin
# @Site    : 
# @File    : image_prcess.py
# @Software: PyCharm
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import numpy as np
import os
import matplotlib.pyplot as plt
import time
import shutil


# reshape the images to a square
def process_img(raw_path, result_path):
    img4 = Image.open(raw_path)
    longer_side = max(img4.size)
    horizontal_padding = (longer_side - img4.size[0]) / 2
    vertical_padding = (longer_side - img4.size[1]) / 2
    img5 = img4.crop(
        (
            -horizontal_padding,
            -vertical_padding,
            img4.size[0] + horizontal_padding,
            img4.size[1] + vertical_padding
        )
    )
    img4.close();
    img5 = img5.resize((512, 512))
    img5.save(result_path)


if __name__ == '__main__':
    # This file reshape the images into specific size, and padding to a square
    train_path = "G:/re/train/"
    # for i in range(1,31):
    #   data_path = train_path + str(i);
    #   result_file = data_path + '/';
    #   files = os.listdir(data_path)
    #   for img_name in files:
    #       img_path = data_path + '/' + img_name;
    #       result_img_path = result_file + '/' + img_name;
    #       process_img(img_path, result_img_path)
    for i in range(1,6):
        files = os.listdir(train_path + str(i))
        for img_name in files:
            process_img(train_path + str(i) + '/' + img_name,train_path + str(i+10) + '/' + img_name)


